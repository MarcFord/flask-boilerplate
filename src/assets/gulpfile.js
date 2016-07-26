/**
 * Created by marc on 6/30/16.
 */
var gulp = require('gulp');
var gutil = require('gulp-util');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var minifycss = require('gulp-minify-css');
var rename = require('gulp-rename');
var gzip = require('gulp-gzip');
var livereload = require('gulp-livereload');

var gzip_options = {
    threshold: '1kb',
    gzipOptions: {
        level: 9
    }
};

var config = {
     sassPath: './scss',
    publicDir: '../static',
    assetsDir: './',
    imagesDir: './images'
};

gulp.task('images', function () {
   return gulp.src(config.imagesDir + '/**.*').pipe(gulp.dest(config.publicDir + '/img'));
});

gulp.task('default', ['images'], function() {
    return gutil.log('Gulp is running!')
});
