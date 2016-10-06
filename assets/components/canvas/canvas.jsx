import React, {PropTypes} from 'react'
import styles from './canvas.scss'

var Canvas = React.createClass({
    updateCanvas: () => {
        "use strict";
        var canvas = this.refs.canvas;
        const ctx = canvas.getContext('2d');
        canvas.width = this.props.newImgWidth;
        canvas.height = this.props.newImgHeight;
        ctx.drawImage(this.props.newImg, 0, 0, canvas.width, canvas.height);
    },
    render: () => {
        // this.updateCanvas();
        return (
            <section className="canvas-wrapper">
                <canvas ref="canvas"></canvas>
            </section>
        );
    }
});

export default Canvas