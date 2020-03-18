## OpenMP - A Multi-Programming Library

### Steps to Create a Parallel Program

1. Include the header file

```
#include <omp.h> // OpenMP header
```

2. Set the number of threads

we can set the number of threads to execute the program using the external variable.

```
export OMP_NUM_THREADS=5
```

We can also set the number of threads using `omp_set_thread_num(num_threads);`.

3. Specify the parallel region

In OpenMP, we need to mention the region which we are going to make it as parallel using the keyword `pragma omp parallel`.
The `pragma omp parallel` is used to fork additional threads to carry out the work enclosed in the parallel.
The original thread will be denoted as the master thread with thread ID 0.
Code for creating a parallel region would be:

```
#pragma omp parallel
{
  // Parallel region code 
}
```

For example:

```
#pragma omp parallel                   
{
    printf("Hello World... from thread = %d\n", 
           omp_get_thread_num());
}
```

Once the compiler encounters the parallel regions code, the master thread (thread which has thread id 0) will fork into the specified number of threads.
Here it will get forked into 5 threads because we will initialise the number of threads to be executed as 5, using the command `export OMP_NUM_THREADS=5`.
Entire code within the parallel region will be executed by all threads concurrently.
Once the parallel region ended, all threads will get merged into the master thread.

4. Compile and run

```
gcc -fopenmp hello.c -o hello
./hello
```

### More References

http://www.bowdoin.edu/~ltoma/teaching/cs3225-GIS/fall16/Lectures/openmp.html
