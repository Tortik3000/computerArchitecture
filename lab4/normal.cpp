#include <iostream>
#include <stdio.h>
#include <omp.h>
#include <cmath>
#include <random>

int main(int argc, char *argv[]) {
    int n;
    int streamCount = std::atoi(argv[1]);
    double point0[3];
    double point1[3];
    double point2[3];

    try {
        FILE *fin = fopen(argv[2], "rb");
        fscanf(fin, "%i", &n);
        fseek(fin, 3, SEEK_CUR);

        for (int i = 0; i < 3; i++) {
            double coord;
            if (i == 0) {
                for (int j = 0; j < 3; j++) {
                    fscanf(fin, "%lf", &coord);
                    point0[j] = coord;
                }
            } else if (i == 1) {
                for (int j = 0; j < 3; j++) {
                    fscanf(fin, "%lf", &coord);
                    point1[j] = coord;
                }
            } else {
                for (int j = 0; j < 3; j++) {
                    fscanf(fin, "%lf", &coord);
                    point2[j] = coord;
                }
            }
            fseek(fin, 4, SEEK_CUR);
        }
        fclose(fin);
    } catch (std::exception exception) {
        std::cout << "File format exception";
    }
    double tstart = omp_get_wtime();


    double edge0[3], edge1[3], edge2[3];
    for (int i = 0; i < 3; i++) {
        edge0[i] = (point1[i] - point0[i]);
        edge1[i] = (point1[i] - point2[i]);
        edge2[i] = (point0[i] - point2[i]);
    }

    double moduleEdge0, moduleEdge1, moduleEdge2;
    moduleEdge0 = sqrt(edge0[0] * edge0[0] + edge0[1] * edge0[1] + edge0[2] * edge0[2]);
    moduleEdge1 = sqrt(edge1[0] * edge1[0] + edge1[1] * edge1[1] + edge1[2] * edge1[2]);
    moduleEdge2 = sqrt(edge2[0] * edge2[0] + edge2[1] * edge2[1] + edge2[2] * edge2[2]);


    double min0 = moduleEdge0;
    if (min0 > moduleEdge1) {
        min0 = moduleEdge1;
    }

    min0 = min0 / sqrt(2);
    if (moduleEdge0 == moduleEdge1 && moduleEdge0 == moduleEdge2) {
        min0 = moduleEdge0 / sqrt(2);
    }
    double v = min0 * min0 * min0 * 8;


    int m = 0;
    if (streamCount != 0) {
        omp_set_num_threads(streamCount);
    }


    std::random_device rd;
#pragma omp parallel\
    if(streamCount != -1)
        {
            std::mt19937 gen(rd());
            int localM = 0;
            double x, y, z;
            if (streamCount == 0) {
                streamCount = omp_get_num_threads();
            }
#pragma omp for schedule(static, 1000)
        for (int i = 0; i < n; i++) {
            x = gen() / 1.0 / UINT32_MAX * 2 * min0 - min0;
            y = gen() / 1.0 / UINT32_MAX * 2 * min0 - min0;
            z = gen() / 1.0 / UINT32_MAX * 2 * min0 - min0;
            if (x < 0) {x = -x;}
            if (y < 0) {y = -y;}
            if (z < 0) {z = -z;}
            if (x + y + z <= min0) {
                localM++;
            }
        }
#pragma omp critical
            {
                m += localM;
            }
        }

    double tend = omp_get_wtime();
    double ans = v * m / n;
    double ansAnalytic = v / 6;


    if (streamCount == -1) {
        streamCount += 1;
    }

    FILE *fout = fopen(argv[3], "wb");
    fprintf(fout, "%g %g\n", ansAnalytic, ans);
    fclose(fout);
    printf("Time (%i thread(s)): %g ms\n", streamCount, (tend - tstart) * 1000);
}