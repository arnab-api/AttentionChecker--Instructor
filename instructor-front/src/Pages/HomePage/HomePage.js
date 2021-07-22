import React, { useState, useEffect, useRef} from "react";
import ReactDOM from "react-dom";
import h337 from "heatmap.js";
import Button from "@material-ui/core/Button";
import CachedIcon from "@material-ui/icons/Cached";
import axios from "axios";

export const HomePage = ({}) => {
    const canvasHeight = 500;
    const canvasWidth = canvasHeight * (16 / 9);

    const [heatmapInstance, setHeatMapInstance] = useState();
    const [heatMapPoints, setHeatmapPoints] = useState([]);

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

    const convertHeatMapPointsForProjection = (heatpoints) => {
        var points = [];
        var max = [];

        for(var idx = 0; idx < heatpoints.length; idx++){
            var val = heatpoints[idx].value
            var max = Math.max(max, val)

            var point = {
                x       : Math.round(heatpoints[idx].x*canvasWidth),
                y       : Math.round(heatpoints[idx].y*canvasHeight),
                value   : val
            }
            points.push(point)
        }

        // heatmap data format
        var data = {
            max: max,
            data: points,
        };

        return data;
    }

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

    const url = "get_current_gaze";
    const refreshHeatCanvas_backend = () => {
        axios.get("/api/"+url)
            .then((response) => {
                console.log(" refresing heatmap from backend >>> ", response.data);
                setHeatmapPoints(response.data);
                let heatmapdata = convertHeatMapPointsForProjection(response.data);
                console.log(heatmapdata)
                populateHeatMap(heatmapInstance, heatmapdata);
            }).catch((error) => {

            });
    };

    const [counter, setCounter] = useState(10)
    let curval = 10
    const countDown = () => {
        console.log("countdown called >> ", curval, counter)
        if(curval == 1){
            curval = 10
            setCounter(10);
            return
        }
        curval -= 1
        setCounter(curval)
    }

    const ref = useRef(null);

    useEffect(() => {
        let tmp = h337.create({
            container: document.querySelector(".HeatmapContainer"),
        });
        setHeatMapInstance(tmp);
        // let heatmapdata = getRandomHeatMap();
        // populateHeatMap(tmp, heatmapdata);
        axios.get("/api/"+url)
            .then((response) => {
                console.log(" gaze heatmap >>> ", response.data);
                setHeatmapPoints(response.data);
                let heatmapdata = convertHeatMapPointsForProjection(response.data);
                console.log(heatmapdata)
                populateHeatMap(tmp, heatmapdata);
            }).catch((error) => {

            });
        setInterval(() => {
            ref.current.click();
          }, 10*1000); //miliseconds
        setInterval(countDown, 1000);
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
                ref = {ref}
                startIcon={<CachedIcon />}
                onClick={refreshHeatCanvas_backend}
            >
                Refresh
            </Button>
            <h1> Refreshig in: {counter} seconds</h1>
        </>
    );
};
