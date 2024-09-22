#include <Servo.h> 
//pwm:(1000-1500-2000)
int pbase=1500;
int parm1=1500;
int parm2=1500;
int pwrist=1500;
int phand=1500;   
Servo servobase;
Servo servoarm1,servoarm2;
Servo servowrist,servohand;

int pstep=100;
void allrest()
{
  servobase.writeMicroseconds(pbase);
  servoarm1.writeMicroseconds(parm1);
  servoarm2.writeMicroseconds(parm2);
  servowrist.writeMicroseconds(pwrist);
  servohand.writeMicroseconds(phand);
  delay(200);
 }

void baseleft()
{
  if (pbase<2300)  pbase+=pstep;
  servobase.writeMicroseconds(pbase);
  delay(200); 
}
void baseright()
{
  if (pbase>700)  pbase-=pstep;
  servobase.writeMicroseconds(pbase);
  delay(200); 
}
void arm1up()
{
  if (parm1<2000)  parm1+=pstep;
  servoarm1.writeMicroseconds(parm1);
  delay(500); 
  }
void arm1down()
{
  if (parm1>1000)  parm1-=pstep;
  servoarm1.writeMicroseconds(parm1);
  delay(50); 
  }

void arm2down()
{
  if (parm2<2000)  parm2+=pstep;
  servoarm2.writeMicroseconds(parm2);
  delay(50); 
  }
void arm2up()
{
  if (parm2>1000)  parm2-=pstep;
  servoarm2.writeMicroseconds(parm2);
  delay(50); 
  }
void wristleft()
{
  if (pwrist<2000)  pwrist+=pstep;
  servowrist.writeMicroseconds(pwrist);
  delay(50);
  }
void wristright()
{
  if (pwrist>1000)  pwrist-=pstep;
  servowrist.writeMicroseconds(pwrist);
  delay(50);
  }
void handopen(){
 if (phand>1000)  phand-=pstep*3;
  servohand.writeMicroseconds(phand);
  delay(50);  
  }
void handclose(){
  if (phand<2000)  phand+=pstep*3;
  servohand.writeMicroseconds(phand);
  delay(50);  
  }
//左右转动
void action1()
{
   allrest();
   delay(1000);
   servobase.writeMicroseconds(2000);
   delay(500);
   servobase.writeMicroseconds(1500);
   delay(500); 
   servobase.writeMicroseconds(1000);
   delay(500); 
   servobase.writeMicroseconds(1500);
   delay(500);   
}
//点头
void action2()
{
  allrest();
  delay(1000);  
  servoarm2.writeMicroseconds(1800);
  delay(500);  
  servoarm2.writeMicroseconds(1200);
  delay(500);
  servoarm2.writeMicroseconds(1500);
  delay(500);
}
//前上，转动手腕
void action3()
{
  allrest();
  delay(1000);
  servowrist.writeMicroseconds(2000);
  delay(500); 
  servowrist.writeMicroseconds(1000);
  delay(500); 
   servowrist.writeMicroseconds(1500);
  delay(500); 
}
//向前伸手，抓取
void action4()
{
   allrest();
   delay(1000);
   servohand.writeMicroseconds(1000);
   delay(500);
   servohand.writeMicroseconds(2000);
   delay(500);
}
