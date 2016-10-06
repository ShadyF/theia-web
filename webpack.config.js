//require our dependencies
var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
    //the base directory (absolute path) for resolving the entry option
    context: __dirname,
    //the entry point we created earlier. Note that './' means
    //your current directory. You don't have to specify the extension  now,
    //because you will specify extensions later in the `resolve` section
    entry: ['bootstrap-loader', './assets/app'],

    output: {
        path: path.resolve('./build/'),
        filename: "[name]-[hash].js"
    },

    plugins: [
        //tells webpack where to store data about your bundles.
        new BundleTracker({filename: './webpack-stats.json'}),
        //makes jQuery available in every module
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        }),
        new ExtractTextPlugin("./styles.css")
    ],

    module: {
        loaders: [
            // Bootstrap 3
            {test: /\.(woff2?|svg)$/, loader: 'url?limit=10000'},
            {test: /\.(ttf|eot)$/, loader: 'file'},
            {test: /bootstrap-sass[\/\\]assets[\/\\]javascripts[\/\\]/, loader: 'imports?jQuery=jquery'},

            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                query: {
                    presets: ['react', 'es2015']
                }
            },
            {
                test: /\.css$/,
                loader: ExtractTextPlugin.extract("style-loader", "css-loader")
            },
            {
                test: /\.scss$/,
                loader: ExtractTextPlugin.extract('css!sass')
            }
        ]
    },

    resolve: {
        //tells webpack where to look for modules
        modulesDirectories: ['node_modules'],
        //extensions that should be used to resolve modules
        extensions: ['', '.js', '.jsx']
    },

    devtool: 'source-map'
};