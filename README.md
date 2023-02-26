# IOT BASED SMART AGRICULTURE TO PROTECT CROP FROM ANIMAL INVASION
                                                                                    

Animal attacks in India are a common story nowadays. Due to the unavailability of any detection these attacks kill villagers and also destroy their crops. Due to lack of proper safety measures, these villagers are left helpless to their fate. Therefore a proper detection could help save their lives and also to the preservation of crops. Also the crops of villagers are destroyed due to frequent interference of animals.The crops and paddy fields cannot be always fenced. So the possibility of crops being eaten away by cows and goats are very much present. This could result in huge wastage of crops produced by the farmers. To making the best use of modern technology , we can prepare a IOT model which protects the crop from an animal invasion. This model gives reliable security and safety to crops, so that the economic losses incurred by our farmers are minimized and they have a good crop yield.


Hardware components used: 

1. Raspberry Pi 3
2. PIR Sensor
3. Pi camera
4. Buzzer

Software Requirements:
1. Backend languages: Python, Flask
2. HTML,CSS,JAVASCRIPT, AJAX

Whenever PIR Sensor sense the presence of animal object ,PI Camera turns on and video streaming starts to find the object. Every frame in Video streaming is given to Object detection algorithm i.e., Mobilenet SSD. After detection if system concludes that there is presence of animal then Buzzer will turns on in order to run away animal from the field. Then message notification is sent to the user about animal intrusion with details. We also converted Raspberry Pi into Server which renders the web page for user to view the video streaming with some good options.


![alt text](images/Architecture_diagram.png)
                                                                         #Architecture Diagram


![alt text](images/Model.jpg)

                                                                                #Model 

![alt text](images/Interface.png)

                                                                           #User Interface 

![alt text](images/Notification.png)

                                                        #Notification received by the former after animal detection. 




