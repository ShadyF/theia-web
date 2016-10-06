import React from 'react'
import style from './bottomnav.scss'

var TransformsTab = React.createClass({
    render: () => {
        return (
            <div role="tabpanel" className="tab-pane active" id="transforms">
                <button type="button" className="btn btn-default btn-tabpane" data-toggle="popover"
                        data-content='<span class="slider-value">0</span>
                <input class="slider-input" data-operation="Rotate"
                type="range" min="-180" max="180" step="1" value="0">'>
                    Rotate
                </button>
            </div>
        )
    }
});

var TintsTab = React.createClass({
    render: function() {
        var tintButtons = this.props.tints.forEach((tint) => {
            return (
                <button type="button" className="btn btn-default tint btn-tabpane" data-operation="Tint"
                        data-tint_name={tint}>
                    {tint}
                </button>
            )
        });
        return (
            <div role="tabpanel" className="tab-pane" id="tints">
                {tintButtons}
            </div>
        )
    }
});

var BottomNav = React.createClass({
    render: () => {
        var tints = ['HEY', 'GURL'];
        return (
            <nav className="navbar navbar-default navbar-fixed-bottom">
                <div className="tab-content">
                    <TransformsTab/>
                    <TintsTab tints={tints}/>
                </div>
                <ul className="nav nav-tabs">
                    <li role="presentation" className="active"><a id="transform-nav-tab" href="#transforms">Transforms</a>
                    </li>
                    <li role="presentation"><a id="tints-nav-tab" href="#tints">Tints</a></li>
                </ul>
            </nav>
        )
    }
});

export default BottomNav;