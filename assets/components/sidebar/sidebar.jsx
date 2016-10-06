import React, {PropTypes} from 'react'
import styles from './sidebar.scss'

var SidebarHeader = React.createClass({
    render: () => {
        return (
            <header>
                <h1>Theia</h1>
                <span>An Online Image Processing Tool</span>
            </header>
        );
    }
});

var Separator = React.createClass({
    render: () => {
        return (
            <div className="seperator"></div>
        );
    }
});

var SidebarButtons = React.createClass({
    render: () => {
        return (
            <div>
                <label className="btn btn-side btn-browse">
                    Browse <input type="file" className="imageLoader" style={{display: 'none'}}/>
                </label>
                <button className="btn btn-side btn-reset" type="button">
                    RESET
                </button>
                <a href="download/" type="button" className="btn btn-download">
                    Download
                </a>
            </div>
        )
    }
});

var SidebarFooter = React.createClass({
    render: () => {
        return (
            <footer>
                <hr/>
                <section className="credits">
                    <small>Created by</small>
                    <span className="hide-xs">·</span>
                    <span className="name">Shady Fanous</span>
                </section>
                <section className="links">
                    <a className="btn  link-btn email" href="mailto:sssfanous@gmail.com">
                        <i className="fa fa-envelope-o" aria-hidden="true"/>
                    </a>
                    <a className="btn link-btn github" href="https://github.com/ShadyF/theia-web">
                        <i className="fa fa-github" aria-hidden="true"/>
                    </a>
                </section>
            </footer>
        )
    }
});

var Sidebar = React.createClass({
    render: () => {
        return (
            <aside className="sidebar-wrapper">
                <section className="sidebar-upper">
                    <SidebarHeader/>
                    <Separator/>
                    <SidebarButtons/>
                    <Separator/>
                </section>
                <SidebarFooter/>
            </aside>
        )
    }
});

export default Sidebar