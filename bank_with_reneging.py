import salabim as sim


class CustomerGenerator(sim.Component):
    def process(self):
        while True:
            Customer()
            self.hold(sim.Uniform(5, 15).sample())


class Customer(sim.Component):
    def process(self):
        if len(waitingline) >= 5:
            env.number_balked += 1
            env.print_trace("", "", "balked")
            print(env.now(), "balked", self.name())
            self.cancel()
        self.enter(waitingline)
        for clerk in clerks:
            clerk: Clerk
            if clerk.ispassive():
                clerk.activate()
                break  # 一个员工服务一个客户
        self.hold(50)
        if self in waitingline:
            self.leave(waitingline)
            env.number_reneged += 1
            env.print_trace("", "", "reneged")
        else:
            self.passivate()


class Clerk(sim.Component):
    def process(self):
        while True:
            while len(waitingline) == 0:
                self.passivate()
            self.customer = waitingline.pop()
            self.customer.activate()  # get the customer out of it's hold(50)
            self.hold(30)
            self.customer.activate()  # signal the customer that's all's done


env = sim.Environment(trace=False)
CustomerGenerator()
env.number_balked = 0  # 队列超过5人，客户停止入队的次数
env.number_reneged = 0  # 客户等待超时提前出队的次数
clerks = sim.Queue("clerks", fill=(Clerk() for _ in range(3)))

waitingline = sim.Queue("waitingline")
env.run(till=300000)
waitingline.length.print_histogram(30, 0, 1)
print("number reneged", env.number_reneged)
print("number balked", env.number_balked)
