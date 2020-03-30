let gulp = require('gulp'),
    sass = require('gulp-sass'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat'),
    rename = require('gulp-rename'),
    del = require('del'),
    htmlmin = require('gulp-htmlmin'),
    imagemin = require('gulp-imagemin'),
    autoprefixer = require('gulp-autoprefixer');


let arrBlock = "base/.blocks/.messages/.users/";

function scss(f) {f();
    arrBlock.split('.').forEach(function(element) {        
        gulp.task('element', function() {
            return gulp.src('code/static/' + element + 'css/*scss')
                .pipe(sass({outputStyle: "compressed"}))
                .pipe(autoprefixer({
                    overrideBrowserslist: ['last 2 versions']
                }))
                .pipe(rename({suffix: '.min'}))
                .pipe(gulp.dest('code/static/' + element + 'css/'))
        });
    });
}

function html(f) {f();
    arrBlock.split('.').forEach(function(element) {        
        gulp.task('element', function() {
            return gulp.src('code/templates/' + element + '*.html')
            .pipe(htmlmin({ collapseWhitespace: true }))
            .pipe(rename({suffix: '.min'}))
            .pipe(gulp.dest('code/templates_min/' + element));
        });
    });
}

function js(f) {f();
    arrBlock.split('.').forEach(function(element) {        
        gulp.task('element', function() {
            return gulp.src('code/static/' + element + 'js/*.js')
            .pipe(uglify())
            .pipe(rename({suffix: '.min'}))
            .pipe(gulp.dest('code/static/' + element + 'js/'))
        });
    });
}

function images(f) {f();
    arrBlock.split('.').forEach(function(element) {        
        gulp.src('code/static/' + element + 'images/*')
        .pipe(imagemin())
        .pipe(gulp.dest('code/static/' + element + 'images_min/'))
    });
}

gulp.task('clean', async function() {
    del.sync('app/index.html');
});

gulp.task('clean', gulp.series('clean'))
gulp.task('default', gulp.series(scss, html, js, images));