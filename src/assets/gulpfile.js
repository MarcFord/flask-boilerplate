/**
 * Created by marc on 6/30/16.
 */
var gulp = require('gulp');
var gutil = require('gulp-util');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var minifycss = require('gulp-minify-css');
var rename = require('gulp-rename');
var livereload = require('gulp-livereload');
var jshint = require('gulp-jshint');
var sourcemaps = require('gulp-sourcemaps');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');

var config = {
     sassPath: './scss',
    publicDir: '../static',
    assetsDir: './',
    imagesDir: './images',
    production: !!gutil.env.production
};

// configure the jshint task
gulp.task('jshint', function() {
  return gulp.src(config.assetsDir + 'js/**/*.js')
    .pipe(jshint())
    .pipe(jshint.reporter('jshint-stylish'));
});

gulp.task('build-js', function() {
  return gulp.src(config.assetsDir + 'js/**/*.js')
    .pipe(sourcemaps.init())
      .pipe(concat('site.js'))
      //only uglify if gulp is ran with '--type production'
      .pipe(config.production ? uglify() : gutil.noop())
    .pipe(!config.production ? sourcemaps.write() : gutil.noop())
    .pipe(gulp.dest(config.publicDir + '/script'));
});

gulp.task('build-css', function() {
  return gulp.src(config.assetsDir + 'scss/**/*.scss')
    .pipe(sass())
    .pipe(gutil.env.type === 'production' ? minifycss() : gutil.noop())
    .pipe(gulp.dest(config.publicDir + '/styles'));
});

gulp.task('bootstrap-fonts', function () {
    return gulp.src(config.assetsDir + 'node_modules/bootstrap-sass/assets/fonts/bootstrap/**.*').pipe(gulp.dest(config.publicDir + '/fonts'));
});

gulp.task('fontawesome-fonts', function () {
    return gulp.src(config.assetsDir + 'node_modules/font-awesome/fonts/**.*').pipe(gulp.dest(config.publicDir + '/fonts'));
});

gulp.task('build-fonts', ['bootstrap-fonts', 'fontawesome-fonts'], function () {
    return gulp.src(config.assetsDir + 'fonts/**/**.*').pipe(gulp.dest(config.publicDir + '/fonts'));
});

gulp.task('images', function () {
   return gulp.src(config.imagesDir + '/**.*').pipe(gulp.dest(config.publicDir + '/img'));
});

gulp.task('default', ['images', 'build-fonts', 'build-js', 'build-css'], function() {
    return gutil.log('Gulp is running!')
});

/* Watch Files For Changes */
gulp.task('watch', ['default'], function() {
    livereload.listen();
    gulp.watch(config.assetsDir + 'scss/**/*.scss', ['build-css']);
    gulp.watch(config.assetsDir + 'js/**/*.js', ['jshint', 'build-js']);

    /* Trigger a live reload on any Django template changes */
    gulp.watch('**/templates/*').on('change', livereload.changed);

});
