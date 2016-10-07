import React from 'react'
import style from './bottomnav.scss'

var TransformsTab = React.createClass({
    checkIfActive: function () {
        return this.props.active ? "active" : "";
    },
    render: function () {
        return (
            <div role="tabpanel" className={"tab-pane " + this.checkIfActive()} id="transforms">
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
    checkIfActive: function () {
        return this.props.active ? "active" : "";
    },
    render: function () {
        var tintButtons = this.props.tints.map(function (tint, id) {
            return (
                <button type="button" key={id} className="btn btn-default tint btn-tabpane" data-operation="Tint"
                        data-tint_name={tint}>
                    {tint}
                </button>
            )
        });
        return (
            <div role="tabpanel" className={"tab-pane " + this.checkIfActive()} id="tints">
                {tintButtons}
            </div>
        )
    }
});

var BottomNav = React.createClass({
    changeActiveTab: function (e) {
        e.preventDefault();
        this.setState({active_tab: e.target.id});
    },
    getInitialState: function () {
        return {active_tab: 'transform-nav-tab'}
    },
    render: function () {
        var tints = ['HEY', 'GURL'];
        return (
            <nav className="navbar navbar-default navbar-fixed-bottom">
                <div className="tab-content">
                    <TransformsTab active={this.state.active_tab == 'transform-nav-tab'}/>
                    <TintsTab tints={tints} active={this.state.active_tab == 'tints-nav-tab'}/>
                </div>
                <ul className="nav nav-tabs">
                    <li role="presentation" className={this.state.active_tab == 'transform-nav-tab'? "active" : ""}><a
                        onClick={this.changeActiveTab} id="transform-nav-tab" href="#transforms">Transforms</a>
                    </li>
                    <li role="presentation" className={this.state.active_tab == 'tints-nav-tab'? "active" : ""}><a
                        onClick={this.changeActiveTab} id="tints-nav-tab" href="#tints">Tints</a></li>
                </ul>
            </nav>
        )
    }
});

export default BottomNav;