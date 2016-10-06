import React from 'react';
import ReactDOM from 'react-dom'
import Sidebar from './components/sidebar/sidebar'
import Canvas from './components/canvas/canvas'
import SidebarToggle from './components/sidebartoggle/sidebartoggle'
import BottomNav from './components/bottomnav/bottomnav'
import style from './global.scss'
const App = React.createClass({
    render: function () {
        return (
            <div id="wrapper">
                <Sidebar/>
                <div id="page-content-wrapper">
                    <div className="container-fluid fill">
                        <Canvas/>
                        <BottomNav/>
                    </div>
                </div>
                <SidebarToggle/>
            </div>
        )
    }
});

ReactDOM.render(
    <App/>, document.getElementById('app')
);