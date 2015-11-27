var gulp = require('gulp');
var typescript = require('gulp-tsc');

gulp.task('default', ['compile:src']);

gulp.task('compile:src', function () {
    return gulp.src(['static/src/**/*.ts'])
        .pipe(typescript({
            out: 'homeAutomation.js',
            target: 'ES5'}))
        .pipe(gulp.dest('static/bin'))
});

gulp.task('watch', function () {
    return gulp.watch('static/src/**/*.ts', ['compile:src']);
});
