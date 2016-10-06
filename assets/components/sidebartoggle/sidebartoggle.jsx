import React from 'react'
import style from './sidebartoggle.scss'

var SidebarToggle = React.createClass({
    render: () => {
        return (<div className="menu-toggle menu-toggle-active" data-menu="2"></div>)
    }
});

export default SidebarToggle;