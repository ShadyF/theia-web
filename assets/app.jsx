import React from 'react';
import ReactDOM from 'react-dom'
import Sidebar from './components/sidebar/sidebar'
import Canvas from './components/canvas/canvas'

const App = React.createClass({
    render: function () {
        return (
            <div>
                <Sidebar/>
                <Canvas/>
            </div>
        )
    }
});

ReactDOM.render(
    <App/>, document.getElementById('app')
);