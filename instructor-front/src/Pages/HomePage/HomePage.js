import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import h337 from "heatmap.js";
import Button from "@material-ui/core/Button";
import CachedIcon from "@material-ui/icons/Cached";

export const HomePage = ({}) => {
    const canvasHeight = 500;
    const canvasWidth = canvasHeight * (16 / 9);

    const [heatmapInstance, setHeatMapInstance] = useState();

    const getRandomHeatMap = (len = 20) => {
        // now generate some random data
        var points = [];
        var max = 0;

        while (len--) {
            var val = Math.floor(Math.random() * 100);
            max = Math.max(max, val);
            var point = {
                x: Math.floor(Math.random() * canvasWidth),
                y: Math.floor(Math.random() * canvasHeight),
                value: val,
            };
            points.push(point);
        }

        // heatmap data format
        var data = {
            max: max,
            data: points,
        };

        return data;
    };

    const populateHeatMap = (heatmapInstance, heatmapdata) => {
        // if you have a set of datapoints always use setData instead of addData
        // for data initialization
        heatmapInstance.setData(heatmapdata);
    };

    const refreshHeatCanvas = () => {
        let heatmapdata = getRandomHeatMap();
        console.log("refreshing heat canvas", heatmapdata)
        populateHeatMap(heatmapInstance, heatmapdata);
    };

    useEffect(() => {
        let tmp = h337.create({
            container: document.querySelector(".HeatmapContainer"),
        });
        setHeatMapInstance(tmp);
        let heatmapdata = getRandomHeatMap();
        populateHeatMap(tmp, heatmapdata);
    }, []);

    return (
        <>
            <div
                className="HeatmapContainer"
                style={{
                    height: canvasHeight,
                    width: canvasWidth,
                    border: "2px solid black",
                }}
            ></div>
            <Button
                startIcon={<CachedIcon />}
                onClick={refreshHeatCanvas}
            >
                Refresh
            </Button>
        </>
    );
};
