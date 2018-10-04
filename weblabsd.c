#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
  FILE * err = freopen("stderr.txt", "w", stderr);

  int rc = daemon(1, 1);
  if (rc) {
    perror("failed to daemonize");
    return EXIT_FAILURE;
  }

  pid_t pid = fork();

  if (pid == 0) {
    rc = execlp("/usr/bin/python", "/usr/bin/python", "/home/miky/Documentos/repos/Weblabs.py/code.py", NULL);
    if (rc) {
      perror("failed to exec python");
      return EXIT_FAILURE;
    }
  } else {
    waitpid(pid, NULL, 0);
  }

  fclose(err);
  
  return EXIT_SUCCESS;
}
