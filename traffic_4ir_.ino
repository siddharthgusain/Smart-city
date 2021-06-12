int Lane1[] = {13,12,11}; // Lane 1 Red, Yellow and Green
int Lane2[] = {10,9,8};// Lane 2 Red, Yellow and Green
int Lane3[] = {7,6,5};// Lane 3 Red, Yellow and Green
int Lane4[] = {4,3,2};// Lane 4 Red, Yellow and Green

int ir1 , ir2 , ir3 , ir4;

void setup() 
{
  Serial.begin(9600);
  for (int i = 0; i < 3; i++)
  {
    pinMode(Lane1[i], OUTPUT); 
    pinMode(Lane2[i], OUTPUT);
    pinMode(Lane3[i], OUTPUT);
    pinMode(Lane4[i], OUTPUT);
  }
  for (int i = 0; i < 3; i++)
  {
    digitalWrite(Lane1[i], LOW); 
    digitalWrite(Lane2[i], LOW);
    digitalWrite(Lane3[i], LOW);
    digitalWrite(Lane4[i], LOW);
  }
  
}

void ir_read(){
  ir1 = analogRead(A0);
  ir2 = analogRead(A1);
  ir3 = analogRead(A2);
  ir4 = analogRead(A3); 

  if (ir1 > 500) ir1 = 1; else ir1 = 0;
  if (ir2 > 500) ir2 = 1; else ir2 = 0;
  if (ir3 > 500) ir3 = 1; else ir3 = 0;
  if (ir4 > 500) ir4 = 1; else ir4 = 0;
  Serial.print(ir1);
  Serial.print("\t");
  Serial.print(ir2);
  Serial.print("\t");
  Serial.print(ir3);
  Serial.print("\t");
  Serial.print(ir4);
  Serial.print("\t");
  Serial.print("\n");
  }
// [0->red,1->yellow,2->green]  //lane1->A0 , lane3->A2 , lane4->A3 , lane2->A1
void loop() 
 {
  
  //IR read
  ir_read();
  // same density flow 
  if((ir1>500 && ir2>500 && ir3>500 && ir4>500) || (ir1<500 && ir2<500 && ir3<500 && ir4<500) ){
    same_density();
    ir_read();
  }

  else{
  // density based flow
     if(ir1>500 && ir2<500 && ir3<500 && ir4<500){
     digitalWrite(Lane3[2], HIGH);
     digitalWrite(Lane1[0], HIGH);
     digitalWrite(Lane4[0], HIGH);
     digitalWrite(Lane2[0], HIGH);
     delay(7000);
    }
    
     if(ir2>500 && ir1<500 && ir3<500 && ir4<500){
     digitalWrite(Lane4[2], HIGH);
     digitalWrite(Lane1[0], HIGH);
     digitalWrite(Lane2[0], HIGH);
     digitalWrite(Lane3[0], HIGH);
     delay(7000);
    }
     
     if(ir3>500 && ir1<500 && ir2<500 && ir4<500){
     digitalWrite(Lane1[2], HIGH);
     digitalWrite(Lane2[0], HIGH);
     digitalWrite(Lane3[0], HIGH);
     digitalWrite(Lane4[0], HIGH);
     delay(7000);
    }
      if(ir4>500 && ir1<500 && ir2<500 && ir3<500){
     digitalWrite(Lane2[2], HIGH);
     digitalWrite(Lane1[0], HIGH);
     digitalWrite(Lane3[0], HIGH);
     digitalWrite(Lane4[0], HIGH);
     delay(7000);
    }  
  }
 }


 void same_density(){
  
    digitalWrite(Lane1[2], HIGH);
    digitalWrite(Lane3[0], HIGH);
    digitalWrite(Lane4[0], HIGH);
    digitalWrite(Lane2[0], HIGH);
    delay(2000);
    digitalWrite(Lane1[2], LOW);
    digitalWrite(Lane3[0], LOW);
    digitalWrite(Lane1[1], HIGH);
    digitalWrite(Lane3[1], HIGH);
    delay(3000);
    
    digitalWrite(Lane1[1], LOW);
    digitalWrite(Lane3[1], LOW);
    digitalWrite(Lane1[0], HIGH);
    digitalWrite(Lane3[2], HIGH);
    delay(2000);
    digitalWrite(Lane3[2], LOW);
    digitalWrite(Lane4[0], LOW);
    digitalWrite(Lane3[1], HIGH);
    digitalWrite(Lane4[1], HIGH);
    delay(3000);
    
    digitalWrite(Lane3[1], LOW);
    digitalWrite(Lane4[1], LOW);
    digitalWrite(Lane3[0], HIGH);
    digitalWrite(Lane4[2], HIGH);
    delay(2000);
    digitalWrite(Lane4[2], LOW);
    digitalWrite(Lane2[0], LOW);
    digitalWrite(Lane4[1], HIGH);
    digitalWrite(Lane2[1], HIGH);
    delay(3000);
    
    digitalWrite(Lane4[1], LOW);
    digitalWrite(Lane2[1], LOW);
    digitalWrite(Lane4[0], HIGH);
    digitalWrite(Lane2[2], HIGH);
    delay(2000);
    digitalWrite(Lane1[0], LOW);
    digitalWrite(Lane2[2], LOW);
    digitalWrite(Lane1[1], HIGH);
    digitalWrite(Lane2[1], HIGH);
    delay(3000);
    
    digitalWrite(Lane2[1], LOW);
    digitalWrite(Lane1[1], LOW);
 }
