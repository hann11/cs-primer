#include <dirent.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    DIR * dp;

    dp = opendir(".");

    struct dirent *d;

    while ((d = readdir(dp)) != NULL) {
        printf("d_name: %s, d_ino: %llu, d_namelen: %d, d_type: %d\n", d->d_name, d->d_ino, d->d_namlen, d->d_type);

    }

    closedir(dp);

    struct stat lst;

    lstat("???", &lst);

    printf("st_dev: %d, st_ino: %d, st_mode: %d, st_nlink: %d, st_uid: %d, st_gid: %d, st_rdev: %d, st_size: %lld, st_blksize: %d, st_blocks: %d, st_atime: %d, st_mtime: %d, st_ctime: %d\n", lst.st_dev, lst.st_ino, lst.st_mode, lst.st_nlink, lst.st_uid, lst.st_gid, lst.st_rdev, lst.st_size, lst.st_blksize, lst.st_blocks, lst.st_atime, lst.st_mtime, lst.st_ctime);


    //readlink of file ???
    char buf[4096];

    readlink("???", buf, 4096);

    for(int i = 0; i < 4096; i++) {
        if (buf[i] == '\0') {
            break;
        }
        if (buf[i] > 31 && buf[i] < 127) {
            printf("%c", buf[i]);
        }
    }


}