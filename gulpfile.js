let gulp = require('gulp'),
    sass = require('gulp-sass'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat'),
    rename = require('gulp-rename'),
    del = require('del'),
    htmlmin = require('gulp-htmlmin'),
    imagemin = require('gulp-imagemin'),
    autoprefixer = require('gulp-autoprefixer');


let arrBlock = "base.blocks.messages.users";

gulp.task('scss', function() {
    return gulp.src('code/static/**/css/*.scss')
        .pipe(sass({outputStyle: "compressed"}))
        .pipe(autoprefixer({
            overrideBrowserslist: ['last 2 versions']
        }))
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('code/static'))
});

gulp.task('html', function() {
    return gulp.src('code/templates/**/*.html')
        .pipe(htmlmin({ collapseWhitespace: true }))
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('code/templates_min'));
})

gulp.task('js', async()=> {
    return gulp.src('code/static/**/js/*.js')
    .pipe(uglify())
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest('code/static/**/js/'));
});

gulp.task('images', async()=> {      
    gulp.src('code/static/**/images/*')
        .pipe(imagemin())
        .pipe(gulp.dest('code/static/**/images_min/'))
});

gulp.task('clean', async function() {
    del.sync('app/index.html');
});

gulp.task('clean', gulp.series('clean'))
gulp.task('default', gulp.series('scss', 'html', 'js', 'images'));

