import getMedian from "../utils.js";

export default function buildLaps(telemetry) {
    const lapTimes = [];
    let currentLapSample = [];

    const laps = [];
    let prevPct = null;
    let lapStart = null;

    for (const sample of telemetry.samples()) {
        const t = sample.getParam("SessionTime")?.value;
        const pct = sample.getParam("LapDistPct")?.value;
        const speed = sample.getParam("Speed")?.value;
        const brake = sample.getParam("Brake")?.value;
        const throttle = sample.getParam("Throttle")?.value;
        const steering = sample.getParam("SteeringWheelAngle")?.value;
        const yawRate = sample.getParam("YawRate")?.value;
        const gear = sample.getParam("Gear")?.value;
        const lapDist = sample.getParam("LapDist")?.value;
        // uncomment these to see the samples you can use
        //const sampleJson = sample.toJSON()
        //console.log("here's sample", sampleJson)      
      if (typeof t !== "number" || typeof pct !== "number" ||  typeof speed !== "number" || 
        typeof brake !== "number" || typeof throttle !== "number" || typeof steering !== "number" || typeof yawRate !== "number" || typeof gear !== "number" || typeof lapDist !== "number") continue;

      currentLapSample.push({ t, pct, speed, brake, throttle, steering, yawRate, gear, lapDist});

      if (prevPct !== null && pct < 0.1 && prevPct > 0.9) {
          if (lapStart !== null) {
            const lapTime = t - lapStart;
            lapTimes.push(lapTime);
            console.log("lapTime", lapTimes);

            const payload = { lapTime, samples: currentLapSample };
            laps.push(payload);
          }

          lapStart = t;
          currentLapSample = [];
        }

      prevPct = pct;
    }

      if (lapTimes.length === 0) {
        return reply.code(400).send({ error: "No laps detected" });
      }

    return laps
    };

export function cleanLaps(laps) {
    const cleanedLaps = []; 
    const median = getMedian(laps);
    for (let l of laps) {
       if (l <= median) {
            cleanedLaps.push({ lapTime: l, samples: samples});
        } 
    }
}
