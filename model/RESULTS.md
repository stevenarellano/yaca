# Results

**C++-only corpus:**

| Model Type                             | k   | Average Hit Rate @k | Mean Reciprocal Rank @k | Mean Average Precision @k | Average NDCG @k |
| -------------------------------------- | --- | ------------------- | ----------------------- | ------------------------- | --------------- |
| Base Model (cpp)                       | 1   | 0.6164              | 0.6164                  | 0.6164                    | 0.6164          |
| adapter_cpp_10_lr0.01_negatives.pth    | 1   | 0.1330              | 0.1330                  | 0.1330                    | 0.1330          |
| adapter_cpp_10_lr0.01_no_negatives.pth | 1   | 0.7425              | 0.7425                  | 0.7425                    | 0.7425          |
| Base Model (cpp)                       | 3   | 0.6707              | 0.6398                  | 0.6398                    | 0.6478          |
| adapter_cpp_10_lr0.01_negatives.pth    | 3   | 0.1943              | 0.1608                  | 0.1608                    | 0.1714          |
| adapter_cpp_10_lr0.01_no_negatives.pth | 3   | 0.7985              | 0.7676                  | 0.7676                    | 0.7756          |
| Base Model (cpp)                       | 10  | 0.7285              | 0.6500                  | 0.6500                    | 0.6689          |
| adapter_cpp_10_lr0.01_negatives.pth    | 10  | 0.2592              | 0.1641                  | 0.1641                    | 0.2361          |
| adapter_cpp_10_lr0.01_no_negatives.pth | 10  | 0.8406              | 0.7788                  | 0.7788                    | 0.8000          |

**Python-only corpus:**

| Model Type                                | k   | Average Hit Rate @k | Mean Reciprocal Rank @k | Mean Average Precision @k | Average NDCG @k |
| ----------------------------------------- | --- | ------------------- | ----------------------- | ------------------------- | --------------- |
| Base Model (python)                       | 1   | 0.7650              | 0.7650                  | 0.7650                    | 0.7650          |
| adapter_python_10_lr0.01_negatives.pth    | 1   | 0.1783              | 0.1783                  | 0.1783                    | 0.1783          |
| adapter_python_10_lr0.01_no_negatives.pth | 1   | 0.8600              | 0.8600                  | 0.8600                    | 0.8600          |
| Base Model (python)                       | 3   | 0.8250              | 0.7931                  | 0.7931                    | 0.8013          |
| adapter_python_10_lr0.01_negatives.pth    | 3   | 0.2583              | 0.2133                  | 0.2133                    | 0.2249          |
| adapter_python_10_lr0.01_no_negatives.pth | 3   | 0.8900              | 0.8733                  | 0.8733                    | 0.8776          |
| Base Model (python)                       | 10  | 0.8517              | 0.7975                  | 0.7975                    | 0.8107          |
| adapter_python_10_lr0.01_negatives.pth    | 10  | 0.3133              | 0.2220                  | 0.2220                    | 0.2439          |
| adapter_python_10_lr0.01_no_negatives.pth | 10  | 0.9183              | 0.8782                  | 0.8782                    | 0.8878          |

**C++ and Python corpus:**

| Model Type                                    | k   | Average Hit Rate @k | Mean Reciprocal Rank @k | Mean Average Precision @k | Average NDCG @k |
| --------------------------------------------- | --- | ------------------- | ----------------------- | ------------------------- | --------------- |
| Base Model (cpp_python)                       | 1   | 0.6733              | 0.6733                  | 0.6733                    | 0.6733          |
| adapter_cpp_python_10_lr0.01_negatives.pth    | 1   | 0.0700              | 0.0700                  | 0.0700                    | 0.0700          |
| adapter_cpp_python_10_lr0.01_no_negatives.pth | 1   | 0.7733              | 0.7733                  | 0.7733                    | 0.7733          |
| Base Model (cpp_python)                       | 3   | 0.7358              | 0.6996                  | 0.6996                    | 0.7089          |
| adapter_cpp_python_10_lr0.01_negatives.pth    | 3   | 0.0950              | 0.0807                  | 0.0807                    | 0.0853          |
| adapter_cpp_python_10_lr0.01_no_negatives.pth | 3   | 0.8325              | 0.7993                  | 0.7993                    | 0.8078          |
| Base Model (cpp_python)                       | 10  | 0.7758              | 0.7041                  | 0.7041                    | 0.7215          |
| adapter_cpp_python_10_lr0.01_negatives.pth    | 10  | 0.1383              | 0.0822                  | 0.0822                    | 0.1012          |
| adapter_cpp_python_10_lr0.01_no_negatives.pth | 10  | 0.8517              | 0.7977                  | 0.7977                    | 0.8110          |
