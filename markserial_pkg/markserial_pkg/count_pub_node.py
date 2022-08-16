import rclpy
from rclpy.node import Node

from markserial_interfaces.msg import Count,Count2    
class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Count, 'Count', 10)    
        self.publisher2_ = self.create_publisher(Count2, 'Count2', 10)  
        timer_period = 1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0.0

    def timer_callback(self):
        msg = Count()   
        # msg2=Count2()                        
        msg.a = str(self.i)  
        # msg2.b= self.i+1
        self.publisher_.publish(msg)
        # self.publisher2_.publish(msg2)
        self.i = self.i-10.01


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()