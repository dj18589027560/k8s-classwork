from locust import HttpUser, between, task
import warnings
warnings.filterwarnings("ignore")


class WebsiteUser(HttpUser):
    wait_time = between(1, 1)

    # @task
    # def detail1(self):
    #     self.client.get("/detail.html?id=a0a4f044-b040-410d-8ead-4de0446aec7e")
    #     self.client.get("/detail.html?id=d3588630-ad8e-49df-bbd7-3167f7efb246")
    #
    # @task(2)
    # def detail2(self):
    #     self.client.get("/detail.html?id=819e1fbf-8b7e-4f6d-811f-693534916a8b")
    #
    # @task(5)
    # def category(self):
    #     self.client.get("/category.html?tags=magic")
    #     self.client.get("/category.html?tags=sport")
    #     self.client.get("/category.html?tags=action")
    #
    # @task(20)
    # def basket(self):
    #     self.client.get("/basket.html")
    #
    # @task(20)
    # def co(self):
    #     self.client.get("/customer-orders.html")

    @task(40)
    def index(self):
        self.client.get("/")
