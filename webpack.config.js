const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    context: __dirname,
    entry: {
        'main': './static/js/main',
        'qrcode': './static/js/qrcode',
        'theme-dark': './static/js/theme-dark',
        'theme-light': './static/js/theme-light',
    },
    output: {
        path: path.resolve('./static/webpack_bundles/'),
        filename: "[name]-[chunkhash].js"
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new MiniCssExtractPlugin({
            filename: "[name]-[chunkhash].css",
        }),
    ],
    module: {
        rules: [
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    // Translates CSS into CommonJS
                    "css-loader",
                    // optimize CSS
                    "postcss-loader",
                    // Compiles Sass to CSS
                    "sass-loader",
                ],
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name]-[chunkhash].[ext]',
                            outputPath: 'fonts/'
                        }
                    }
                ]
            },
        ],
    },
}
