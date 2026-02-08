import path from "node:path";
import { pipeline } from "node:stream/promises";
import { createWriteStream } from "node:fs";
import fs from "node:fs/promises";
import { Telemetry } from "ibt-telemetry";
import { sendParsedIbt } from "../api/parsedTelemtryApi.js";

const TEMP_IBT_DIR = path.resolve("server-js/tmp/ibt");

export default async function ibtRoutes(fastify, opts) {
  fastify.post("/parseIbt", async (request, reply) => {
    const file = await request.file();
    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    const outPath = path.join(TEMP_IBT_DIR, `${id}.ibt`);
    
    fastify.log.info({ outPath, original: file.filename }, "Saving upload to temp");
    
    try {
      await pipeline(file.file, createWriteStream(outPath));
      fastify.log.info({ outPath }, "Upload saved, ready to parse");
      
      const telemetry = await Telemetry.fromFile(outPath);
      
      // DUMP FULL SESSION INFO
      console.log("\n=== FULL SESSION INFO DUMP ===");
      console.log(JSON.stringify(telemetry.sessionInfo, null, 2));
      
      const sessionInfo = telemetry.sessionInfo.SessionInfo;
      
      console.log("\n=== SESSION INFO SUMMARY ===");
      console.log("Current session:", sessionInfo.CurrentSessionNum);
      console.log("Available sessions:");
      sessionInfo.Sessions.forEach(s => {
        console.log(`  - Session ${s.SessionNum}: ${s.SessionType} (${s.SessionName})`);
      });

      // COLLECT ALL SAMPLES ONCE
      const allSamples = [];
      for (const sample of telemetry.samples()) {
        allSamples.push(sample.toJSON());
      }
      
      console.log(`\nTotal samples collected: ${allSamples.length}`);

      // DEBUG: Check first and last samples
      console.log("\n=== FIRST 5 SAMPLES ===");
      for (let i = 0; i < Math.min(5, allSamples.length); i++) {
        const s = allSamples[i];
        console.log(`Sample ${i}:`, {
          SessionNum: s.SessionNum?.value,
          SessionState: s.SessionState?.value,
          SessionTime: s.SessionTime?.value,
          Lap: s.Lap?.value,
          LapDistPct: s.LapDistPct?.value,
        });
      }
      
      console.log("\n=== LAST 5 SAMPLES ===");
      for (let i = Math.max(0, allSamples.length - 5); i < allSamples.length; i++) {
        const s = allSamples[i];
        console.log(`Sample ${i}:`, {
          SessionNum: s.SessionNum?.value,
          SessionState: s.SessionState?.value,
          SessionTime: s.SessionTime?.value,
          Lap: s.Lap?.value,
          LapDistPct: s.LapDistPct?.value,
        });
      }

      // GROUP BY SESSION
      const sessionGroups = {};
      allSamples.forEach(s => {
        const sessionNum = s.SessionNum.value;
        if (!sessionGroups[sessionNum]) {
          sessionGroups[sessionNum] = [];
        }
        sessionGroups[sessionNum].push(s);
      });

      console.log("\n=== SAMPLES PER SESSION ===");
      Object.entries(sessionGroups).forEach(([sessionNum, samples]) => {
        console.log(`  Session ${sessionNum}: ${samples.length} samples`);
      });

      console.log("\n=== SESSION DETAILS ===");
      Object.entries(sessionGroups).forEach(([sessionNum, samples]) => {
        const first = samples[0];
        const last = samples[samples.length - 1];
        const speeds = samples.map(s => s.Speed.value);
        const maxSpeed = Math.max(...speeds);
        const lapPcts = samples.map(s => s.LapDistPct.value);
        const minLapPct = Math.min(...lapPcts);
        const maxLapPct = Math.max(...lapPcts);
        const laps = samples.map(s => s.Lap.value);
        const minLap = Math.min(...laps);
        const maxLap = Math.max(...laps);
        
        console.log(`\nSession ${sessionNum}:`);
        console.log(`  Duration: ${first.SessionTime.value.toFixed(1)}s - ${last.SessionTime.value.toFixed(1)}s`);
        console.log(`  Max speed: ${maxSpeed.toFixed(1)} m/s (${(maxSpeed * 3.6).toFixed(1)} km/h)`);
        console.log(`  LapDistPct range: ${minLapPct.toFixed(3)} - ${maxLapPct.toFixed(3)}`);
        console.log(`  Lap field: ${minLap} - ${maxLap}`);
        
        let wraps = 0;
        for (let i = 1; i < samples.length; i++) {
          if (samples[i].LapDistPct.value < 0.1 && samples[i-1].LapDistPct.value > 0.9) {
            wraps++;
          }
        }
        console.log(`  Detected lap wraps: ${wraps}`);
      });

      const raceSession = sessionInfo.Sessions.find(
        s => s.SessionType === "Race"
      );
      
      if (!raceSession) {
        console.log("\n❌ No race session found in session info");
        return { error: "No race session found" };
      }

      const RACE_SESSION_NUM = raceSession.SessionNum;
      const raceSamples = sessionGroups[RACE_SESSION_NUM] || [];
      
      console.log(`\n=== PROCESSING RACE SESSION ${RACE_SESSION_NUM} ===`);
      console.log(`Race samples: ${raceSamples.length}`);

      if (raceSamples.length === 0) {
        console.log("❌ No samples found for race session!");
        console.log("\nAvailable session numbers in telemetry:", Object.keys(sessionGroups));
        console.log("Looking for session number:", RACE_SESSION_NUM);
        return { error: "No race data" };
      }

      // DETECT LAPS
      const laps = [];
      let prevLapDistPct = 0;
      let currentLapStart = null;
      let currentLapData = [];

      raceSamples.forEach((data, i) => {
        const time = data.SessionTime.value;
        const lapPct = data.LapDistPct.value;
        const speed = data.Speed.value;
        const brake = data.Brake?.value || 0;
        const throttle = data.Throttle?.value || 0;

        const point = {
          t: time,
          dist: lapPct,
          speed,
          brake,
          throttle,
        };

        // Detect lap completion (wrap around from ~1.0 to ~0.0)
        if (lapPct < 0.1 && prevLapDistPct > 0.9) {
          if (currentLapStart !== null) {
            const lapTime = time - currentLapStart;
            laps.push({
              lapNumber: laps.length + 1,
              lapTime,
              startTime: currentLapStart,
              endTime: time,
              telemetry: currentLapData,
            });
            console.log(`✓ Lap ${laps.length} completed: ${lapTime.toFixed(3)}s (sample ${i})`);
          } else {
            console.log(`⚠ First lap wrap detected at sample ${i}, starting lap timer`);
          }
          currentLapStart = time;
          currentLapData = [];
        }

        currentLapData.push(point);
        prevLapDistPct = lapPct;
      });

      // Analytics
      if (laps.length > 0) {
        const lapTimes = laps.map(l => l.lapTime);
        const fastest = Math.min(...lapTimes);
        const average = lapTimes.reduce((a, b) => a + b, 0) / lapTimes.length;
        
        console.log(`\n=== LAP SUMMARY ===`);
        console.log(`Total laps: ${laps.length}`);
        console.log(`Fastest lap: ${fastest.toFixed(3)}s`);
        console.log(`Average lap: ${average.toFixed(3)}s`);
        
        await sendParsedIbt({
          sessionInfo: raceSession,
          laps,
          summary: {
            totalLaps: laps.length,
            fastestLap: fastest,
            averageLap: average,
          }
        });
        
        return { 
          savedTo: outPath, 
          filename: file.filename,
          lapsDetected: laps.length,
          fastestLap: fastest,
          averageLap: average,
        };
      } else {
        console.log("\n❌ No complete laps detected in race session");
        console.log("This could mean:");
        console.log("  - Session ended before completing a lap");
        console.log("  - LapDistPct doesn't wrap properly");
        console.log("  - Check the 'Lap' field instead of LapDistPct");
        
        return { 
          error: "No laps detected",
          raceSamples: raceSamples.length,
        };
      }
      
    } finally {
      await fs.unlink(outPath).catch(() => {});
    }
  });
}
