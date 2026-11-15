import { test, describe } from "node:test";
import assert from "node:assert/strict";
import getMedian from "../utils.js";

describe("getMedian", () => {
    test("odd length returns the middle value", () => {
        assert.equal(getMedian([5, 1, 3]), 3);
    });

    test("even length returns the average of the two middle values", () => {
        assert.equal(getMedian([4, 1, 3, 2]), 2.5);
    });

    test("sorts numerically, not as strings", () => {
        assert.equal(getMedian([10, 9, 100]), 10);
    });

    test("does not modify the input array", () => {
        const input = [3, 1, 2];
        getMedian(input);
        assert.deepEqual(input, [3, 1, 2]);
    });
});
