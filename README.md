# Machine Learning Engineering 2025/2026
To start the application locally run
> docker compose up

Entire application can take up to 13.5 GBs of VRAM and not all gpus can work with it. That's why model hotswapping was used.
If you believe you don't have enough VRAM to run the application, you can pass the environment variable that will enable model hotswapping between memory and GPU.
> INSUFFICIENT_VRAM=true docker compose up

Or change its value in docker compose file.

Running application was exported to Docker Hub, you can pull it by running
> docker pull dbarania/ium_summary_app

Running it will create logs directory ./summary_log/  