# Results

| Model Type                                  | k   | Average Hit Rate @k | Mean Reciprocal Rank @k | Mean Average Precision @k | Average NDCG @k |
| ------------------------------------------- | --- | ------------------- | ----------------------- | ------------------------- | --------------- |
| Base Model                                  | 1   | 0.6164              | 0.6164                  | 0.6164                    | 0.6164          |
| adapters/adapter_5_no_negatives.pth         | 1   | 0.6374              | 0.6374                  | 0.6374                    | 0.6374          |
| adapters/adapter_5_negatives.pth            | 1   | 0.0350              | 0.0350                  | 0.0350                    | 0.0350          |
| adapters/adapter_10_lr0.01_negatives.pth    | 1   | 0.1330              | 0.1330                  | 0.1330                    | 0.1330          |
| adapters/adapter_10_lr0.01_no_negatives.pth | 1   | 0.7425              | 0.7425                  | 0.7425                    | 0.7425          |
| Base Model                                  | 2   | 0.6514              | 0.6269                  | 0.6269                    | 0.6333          |
| adapters/adapter_10_lr0.01_negatives.pth    | 2   | 0.1803              | 0.1602                  | 0.1602                    | 0.1688          |
| adapters/adapter_10_lr0.01_no_negatives.pth | 2   | 0.7793              | 0.7609                  | 0.7609                    | 0.7657          |
| Base Model                                  | 3   | 0.6707              | 0.6398                  | 0.6398                    | 0.6478          |
| adapters/adapter_5_no_negatives.pth         | 3   | 0.7022              | 0.6663                  | 0.6663                    | 0.6756          |
| adapters/adapter_5_negatives.pth            | 3   | 0.0665              | 0.0484                  | 0.0484                    | 0.0550          |
| adapters/adapter_10_lr0.01_negatives.pth    | 3   | 0.1943              | 0.1608                  | 0.1608                    | 0.1714          |
| adapters/adapter_10_lr0.01_no_negatives.pth | 3   | 0.7985              | 0.7676                  | 0.7676                    | 0.7756          |
| Base Model                                  | 10  | 0.7285              | 0.6500                  | 0.6500                    | 0.6689          |
| adapters/adapter_5_no_negatives.pth         | 10  | 0.7740              | 0.6896                  | 0.6896                    | 0.7100          |
| adapters/adapter_5_negatives.pth            | 10  | 0.1015              | 0.0469                  | 0.0469                    | 0.0658          |
| adapters/adapter_10_lr0.01_negatives.pth    | 10  | 0.2592              | 0.1641                  | 0.1641                    | 0.2361          |
| adapters/adapter_10_lr0.01_no_negatives.pth | 10  | 0.8406              | 0.7788                  | 0.7788                    | 0.8000          |
