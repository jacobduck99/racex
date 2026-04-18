import getMedian from "../utils.js";

const checkNum = (currentValue) => typeof currentValue === "number";

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
        const lat = sample.getParam("Lat")?.value;
        const long = sample.getParam("Long")?.value;
        // uncomment these to see the samples you can use
        //const sampleJson = sample.toJSON()
        //console.log("here's sample", sampleJson)      
    const samples = { t, pct, speed, brake, throttle, steering, yawRate, gear, lapDist, lat, long};
 
    const checkValues = Object.values(samples).every(checkNum);

    if (!checkValues) continue;

    currentLapSample.push(samples);

    if (prevPct !== null && pct < 0.1 && prevPct > 0.9) {
      if (lapStart !== null) {
        const lapTime = t - lapStart;
        lapTimes.push(lapTime);

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
    const times = laps.map((l) => l["lapTime"]);

    const median = getMedian(times);

    for (let t of laps) {
        if (t["lapTime"] <= median) {
            cleanedLaps.push(t);
        }
    }
    return cleanedLaps
}
