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
        // printf("%s\n", d->d_name);
        int fd = open(d->d_name, O_RDONLY);
        if (fd < 0) {
            perror("open");
            return 1;
        }
        struct stat st;
        lstat(d->d_name, &st);
        printf("d_name: %s, Size: %lld, blocks: %lld, on disk: %lld, inode: %lld\n", d->d_name, st.st_size, st.st_blocks, st.st_blocks * 512, st.st_ino);
        printf("st_dev: %d, st_ino: %d, st_mode: %d, st_nlink: %d, st_uid: %d, st_gid: %d, st_rdev: %d, st_size: %lld, st_blksize: %d, st_blocks: %d, st_atime: %d, st_mtime: %d, st_ctime: %d\n", st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_uid, st.st_gid, st.st_rdev, st.st_size, st.st_blksize, st.st_blocks, st.st_atime, st.st_mtime, st.st_ctime);
        // other stat info; 

        close(fd);
    }

    closedir(dp);

}