var gulp = require('gulp');
var typescript = require('gulp-tsc');

gulp.task('default', ['compile:src']);

gulp.task('compile:src', function () {
    return gulp.src(['src/ts/**/*.ts'])
        .pipe(typescript({
            out: 'homeAutomation.js',
            target: 'ES5'}))
        .pipe(gulp.dest('static/js'))
});

gulp.task('watch', function () {
    return gulp.watch('src/ts/**/*.ts', ['compile:src']);
});
