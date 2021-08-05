import React, { useState, useEffect, useRef} from "react";
import ReactDOM from "react-dom";
import h337 from "heatmap.js";
import Button from "@material-ui/core/Button";
import CachedIcon from "@material-ui/icons/Cached";
import axios from "axios";

export const HomePage_sim = () => {
    const canvasHeight = 500;
    const canvasWidth = canvasHeight * (16 / 9);

    const [heatmapInstance, setHeatMapInstance] = useState();
    const [heatMapPoints, setHeatmapPoints] = useState([]);

    const convertHeatMapPointsForProjection = (heatpoints) => {
        var points = [];
        var max = [];

        for(var idx = 0; idx < heatpoints.length; idx++){
            var val = heatpoints[idx].value
            max = Math.max(max, val)

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

    const clearGazeContainerBackend = () => {
        componentDidMount()
        axios.get("/api/clearGazeContainer")
            .then((response) => {
                console.log("clearing gaze container")
            }).catch((error) => {

            })
    }
    
    const saveGazeContainerBackend = () => {
        axios.get("/api/save_gaze")
            .then((response) => {
                console.log("saving current gaze")
            }).catch((error) => {

            })
    }

    useEffect(() => {
        let tmp = h337.create({
            container: document.querySelector(".HeatmapContainer"),
            // radius: 10,
            // maxOpacity: .5,
            // minOpacity: 0,
            // blur: .75,
            // gradient: {
            //   // enter n keys between 0 and 1 here
            //   // for gradient color customization
            //   '.5': 'blue',
            //   '.8': 'red',
            //   '.95': 'white'
            // }
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
    }, []);

    const componentDidMount = () => {
        // var c = document.getElementsByClassName("heatmap-canvas");
        // var ctx = c.getContext("2d");
        // ctx.beginPath();
        // ctx.moveTo(0, 0);
        // ctx.lineTo(300, 150);
        // ctx.stroke();

        var ctx = document.getElementById('grid').getContext('2d');
        // ctx.fillStyle = "rgb(200,0,0)";
        ctx.strokeStyle = 'black';
        ctx.beginPath();    
        for (var x = 0, i = 0; i < 3; x+=canvasWidth/3, i++) {
            for (var y = 0, j=0; j < 3; y+=canvasHeight/3, j++) {            
                ctx.strokeRect (x, y, canvasWidth/3, canvasHeight/3);
            }
        }
        // ctx.fill();
        // ctx.moveTo(0, 0);
        // ctx.lineTo(canvasWidth, canvasHeight);
        ctx.closePath();
    }
    

    return (
        <>
            <div
                className="HeatmapContainer"
                id="heatmap"
                style={{
                    height: canvasHeight,
                    width: canvasWidth,
                    border: "2px solid black",
                }}   
            >
                <canvas id="grid" width={canvasWidth} height={canvasHeight}/>
            </div>
            <Button 
                startIcon={<CachedIcon />}
                onClick={refreshHeatCanvas_backend}
            >
                Refresh
            </Button>
            <Button 
                onClick={clearGazeContainerBackend}
            >
                Re-Initialize
            </Button>
            <Button 
                onClick={saveGazeContainerBackend}
            >
                Save Gaze
            </Button>
        </>
    );
};
