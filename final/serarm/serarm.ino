//USB串口控制机械臂简单动作
//jibotarm,p3-base,p5-arm1,p6-arm2,p9-arm3(未接),p10-wrist,p11-hand
#include "myservo.h"
#define LED 13
char cont;
String comdata = "";
void setup(void)
{
  pinMode(LED, OUTPUT);
  Serial.begin(9600);  
  while(Serial.read()>= 0){}   
  servobase.attach(3);
  servoarm1.attach(5);      //链接舵机
  servoarm2.attach(6);
  servowrist.attach(9);
  servohand.attach(10);
  allrest();  
  delay(100);
  Serial.println("Hello,my robot arm!");
}

void loop(void)
{
   comdata = "";   
   while(Serial.available()){ //当串口有信息传入时开始接收数据
      delay(10); // 等待数据传完
      comdata = Serial.readString();
      //Serial.println(comdata);
      cont=comdata[0];
      Serial.print(cont);      
        switch (cont)
        {
          case 'r':
          {                            
               Serial.println("Baseright is running!");
               baseright(); 
               break;
           }
                               
          case'l':  
          {
               Serial.println("Baseleft is running!");
               baseleft();               
               break;
          }      
          case'd':
          {
               Serial.println("Arm12down() is running!");
               arm1down();
               arm2down();
               break;
          }        
          case'u':
          {
               Serial.println("Arm12up() is running!");
               arm1up();
               arm2up();
               break;
          }           
          //wrist逆时针     
          case'n':
          {
               Serial.println("Wristleft() is running!");
               wristleft();
               break;
          }
          //顺时针        
          case's':
          {
               Serial.println("Wristrigt() is running!");
               wristright();
               break;
          } 
          case'c':
          {
               Serial.println("Handclose() is running!");
               handclose();
               break;
          }        
          case'o':
          {
               Serial.println("Handopen() is running!");
               handopen();
               break;
          }  
           //动作1     
          case'1':
          {
               Serial.println("Action1() is running!");
               action1();
               action1();
               break;
          }
                  
          case'2':
          {
               Serial.println("Action2() is running!");
               action2();
               action2();
               action2();
               break;
          } 
          case'3':
          {
               Serial.println("Action3() is running!");
               action3();
               action3();
               action3();
               break;
          }        
          case'4':
          {
               Serial.println("Action4() is running!");
               action4();
               action4();
               break;
          } 
          case'5':
          {
               Serial.println("Action5() is running!");
               action1();
               action2();
               action3();
               action4();
               break;
          }   
        Serial.flush();
    }
    delay(50);    
     
}
}
//Jibot单个舵机步进控制函数在myservo.cpp
//编写几个完整动作函数，视觉手势1，2，3，4，5分别对应五个定义动作




/*
//欧鹏机械臂函数，供参考
void armupright(){
  arm3stre();
  arm12up();
 
}
void armbow(){
  
}
void armrest(){
  arm12forword();
  arm3back();
}

void arm12forword()//大臂侧向前
{
  armservo1.writeMicroseconds(600);
  armservo2.writeMicroseconds(2400);  
  delay(1000);   
}
void arm12up()//大臂向上，竖直向不一定是1500
{
  armservo1.writeMicroseconds(1500);
  armservo2.writeMicroseconds(1500);  
  delay(1000);  
}
void arm3stre()//小臂伸直
{
  armservo3.writeMicroseconds(1500);
  delay(1000);  
}
void arm3forw()//小臂向前弯曲
{
  armservo3.writeMicroseconds(600);
  delay(1000);
}
void arm3back()//小臂后仰
{
  armservo3.writeMicroseconds(2400);
  delay(5000);
}
*/
