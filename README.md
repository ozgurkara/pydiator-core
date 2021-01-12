
[![](https://img.shields.io/pypi/pyversions/pydiator-core.svg)](https://pypi.org/project/pydiator-core/) ![example event parameter](https://github.com/ozgurkara/pydiator-core/workflows/CI/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/ozgurkara/pydiator-core/badge.svg?branch=master)](https://coveralls.io/github/ozgurkara/pydiator-core?branch=master)  [![](https://img.shields.io/pypi/wheel/pydiator-core.svg)](https://pypi.org/project/pydiator-core/) [![](https://img.shields.io/pypi/format/pydiator-core.svg)](https://pypi.org/project/pydiator-core/)

# Installation

https://pypi.org/project/pydiator-core/

add your requirements.txt ***pydiator-core*** or run the ***pip install pydiator-core*** command

# Examples 

Directly : https://github.com/ozgurkara/pydiator-core/blob/master/examples/main.py

Fastapi : https://github.com/ozgurkara/fastapi-pydiator

# What is the pydiator?
Pydiator is an in-app communication method. 

It provides that developing the code as an aspect. Also, it supports clean architecture infrastructure

It is using design patterns such as chain of responsibility, mediator, singleton.

Pydiator provides which advantages to developers and project?
* Testable
* Use case support
* Aspect programming (Authorization, Validation, Cache, Logging, Tracer etc.) support
* Clean architecture
* Expandable architecture via pipeline
* Independent framework
* SOLID principles
* Has publisher subscriber infrastructure
 
![pydiator](https://raw.githubusercontent.com/ozgurkara/pydiator-core/master/assets/pydiator_flow.png)

# How it works? 
Pydiator knows 4 object types. 
These are;

**1- Request object** 
   * Is used for calling the use case.
   * It should be inherited from **BaseRequest**
   ```python 
    class GetSampleByIdRequest(BaseRequest):
        def __init__(self, id: int):
            self.id = id
   ```
<hr>

**2- Response object**
   * Is used for returning from use case
   * It should be inherited from **BaseResponse**
   ```python
   class GetSampleByIdResponse(BaseResponse):
        def __init__(self, id: int, title: str):
            self.id = id
            self.title = title 
   ``` 

<hr>

**3- Use Case**
   * Includes logic codes    
   * It should be inherited from **BaseHandler**
   * It takes one parameter to handle. The parameter should be inherited **BaseRequest** 
   ```python
   class GetSampleByIdUseCase(BaseHandler):
        async def handle(self, req: GetSampleByIdRequest):
            # related codes are here such as business
            return GetSampleByIdResponse(id=req.id, title="hello pydiatr")     
   ``` 

<hr>

**What is the relation between these 3 object types?**

Every use case object only knows a request object

Every request object is only used by one use case object

<br/>

**How is the use case run?**

Should be had a particular map between the request object and the use case object.

Mapping example;
```python
    def set_up_pydiator():
        container = MediatrContainer()
        container.register_request(GetSampleByIdRequest, GetSampleByIdUseCase())
        #container.register_request(xRequest, xUseCase())
        pydiator.ready(container=container)
```

Calling example;
```python
    await pydiator.send(GetByIdRequest(id=1))
````
or
```python    
    loop = asyncio.new_event_loop()
    response: GetByIdResponse = loop.run_until_complete(pydiator.send(GetByIdRequest(id=1)))
    loop.close()
    print(response.to_json())
```

<hr>

**4- Pipeline**

The purpose of the pipeline is to manage the code as an aspect. 
For instance, you want to write a log for the request and the response of every use case. You can do it via a pipeline easily. You can see the sample log pipeline at this link.

You can create a lot of pipelines such as cache pipeline, validation pipeline, tracer pipeline, authorization pipeline etc. 

Also, you can create the pipeline much as you want but you should not forget that every use case will be used in this pipeline.

<br/>

You can add the pipeline to pipelines such as;
```python
    def set_up_pydiator():
        container = MediatrContainer()        
        container.register_pipeline(LogPipeline())
        #container.register_pipeline(xPipeline())
        pydiator.ready(container=container)
````
<br/>

***How can you write a custom pipeline?***
   * Every pipeline  should be inherited ***BasePipeline***
   * Sample pipeline
```python
    class SamplePipeline(BasePipeline):
        def __init__(self):
            pass
    
        async def handle(self, req: BaseRequest) -> object:
            
            # before executed pipeline and uce case

            response = await self.next().handle(req)
    
            # after executed next pipeline and use case            

            return response
```   


# How to use the notification-subscriber feature

***What is the notification-subscriber feature?***

This feature runs as pub-sub design pattern.

**What is the pub-sub pattern?**

publish-subscribe is a messaging pattern where senders of messages, called publishers, do not program the messages to be sent directly to specific receivers, called subscribers, but instead, categorize published messages into classes without knowledge of which subscribers if any, there may be. Similarly, subscribers express interest in one or more classes and only receive messages that are of interest, without knowledge of which publishers, if any, there are.
<br/>

**How to use this pattern with the pydiator?**

You can see the details that via this link https://github.com/ozgurkara/pydiator-core/blob/master/examples/notification.py

```python
def set_up_pydiator():
    container = MediatrContainer()
    container.register_notification(SampleNotification, [Sample1Subscriber(), Sample2Subscriber(),
                                                             Sample3Subscriber()])
    pydiator.ready(container=container)

if __name__ == "__main__":
    set_up_pydiator()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(pydiator.publish(SamplePublisherRequest(id=1)))
    loop.close()
```


# How to run the Unit Tests
`install tests/requirements.txt`

`pytest tests/`

