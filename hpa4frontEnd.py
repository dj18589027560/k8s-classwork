import time
from kubernetes import client, config
from prometheus_api_client import PrometheusConnect
from k8sLink import api_instance

# 加载 kubeconfig 文件
config.load_kube_config(config_file="kubeconfig.yaml")

# Prometheus服务器的地址
prometheus_url = 'http://192.168.48.100:30003'

# 创建一个Prometheus连接
prometheus = PrometheusConnect(url=prometheus_url)

# 或者，如果在集群中，可以使用以下方法加载 in-cluster 配置
# config.load_incluster_config()

# 创建 Kubernetes API 客户端
autoscaling_api = client.AppsV1Api()
core_api = client.CoreV1Api()

# 定义 namespace 和 deployment 名称
namespace = "sock-shop"
deployment_name = "front-end"


# 定义 CPU 利用率阈值
high_cpu_threshold = 0.7
low_cpu_threshold = 0.3

def get_cpu_usage_percent():
    # 获取 Pod 的 CPU 利用率百分比
    query = 'sum(irate(container_cpu_usage_seconds_total{namespace="sock-shop", container!="",pod=~"front-end.*"}[1m]))'
    result = prometheus.custom_query(query=query)
    #cpu_usage_percent = float(result[0]['value'][1])
    #print(result)
    for data in result:
        if data['value'][1] != '0':
            print(float(data['value'][1]) * 1000)
            return float(data['value'][1]) * 1000
        return float(data['value'][1]) * 1000


def scale_deployment(replica_count):
    # 缩放 Deployment
    # 获取 Deployment 的当前状态
    deployment = autoscaling_api.read_namespaced_deployment(name=deployment_name, namespace=namespace)

    # 更新 Deployment 的副本数
    deployment.spec.replicas = replica_count

    # 应用更新
    autoscaling_api.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)

    #deployment = autoscaling_api.read_namespaced_horizontal_pod_autoscaler(name=f"{deployment_name}-hpa", namespace=namespace)
    #deployment.spec.max_replicas = replica_count
    #deployment.spec.min_replicas = replica_count
    #autoscaling_api.replace_namespaced_horizontal_pod_autoscaler(name=f"{deployment_name}-hpa", namespace=namespace, body=deployment)

while True:
    try:
        # 获取 Deployment 的当前副本数
        deployment = autoscaling_api.read_namespaced_deployment(name=deployment_name, namespace=namespace)

        current_replicas = deployment.spec.replicas

        # 获取 Pod 列表
        #pods = core_api.list_namespaced_pod(namespace=namespace, label_selector=f"app={deployment_name}").items

        # 计算平均 CPU 利用率
        cpu_percent = get_cpu_usage_percent() / (300*current_replicas)
        print(cpu_percent)
        # 根据 CPU 利用率调整副本数
        if cpu_percent >= high_cpu_threshold and current_replicas < 9:
            new_replicas = current_replicas + 1
            scale_deployment(new_replicas)
            print(f"Scaling up to {new_replicas} replicas due to high CPU usage ({cpu_percent}%).")
        elif cpu_percent <= low_cpu_threshold and current_replicas > 1:
            new_replicas = current_replicas - 1
            scale_deployment(new_replicas)
            print(f"Scaling down to {new_replicas} replicas due to low CPU usage ({cpu_percent}%).")
        else:
            print("warning:max replicas")

        # 休眠一段时间再进行下一次检查
        time.sleep(3)
    except Exception as e:
        print(f"Error: {e}")
        # 发生错误时继续进行下一次检查
        time.sleep(3)
