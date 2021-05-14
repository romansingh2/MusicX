const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: "./src/index.js", //entry point is in source directory in index.js
  output: {
    path: path.resolve(__dirname, "./static/frontend"),
    filename: "[name].js", //put output file in statc/frontend in a js file
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },
  optimization: {
    minimize: true, //take javascript and make it smaller, ie getting rid of white spaces and info you dont need. This will speed up loading in the browser
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env": {
        // This has effect on the react lib size
        NODE_ENV: JSON.stringify("production"),
      },
    }),
  ],
};