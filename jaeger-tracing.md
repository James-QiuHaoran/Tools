## Jaeger

Jaeger, inspired by Dapper and OpenZipkin, is a distributed tracing system released as open source by Uber Technologies.
It is used for monitoring and troubleshooting microservices-based distributed systems, including:
- Distributed context propagation
- Distributed transaction monitoring
- Root cause analysis
- Service dependency analysis
- Performance or latency optimization

### Instrumentation

https://www.jaegertracing.io/docs/1.17/client-libraries/

All Jaeger client libraries support the OpenTracing APIs for instrumentation.

### Running Jaeger All-in-One

https://www.jaegertracing.io/docs/1.17/getting-started/#all-in-one

All-in-one is an executable designed for quick local testing, launches the Jaeger UI, collector, query, and agent, with an in memory storage component.
The simplest way to start the all-in-one is to use the pre-built image published to DockerHub (a single command line).

```
$ docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 14250:14250 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.17
```

In Kubernetes: https://github.com/jaegertracing/jaeger-operator

### API

Doc: https://www.jaegertracing.io/docs/1.17/apis/

#### Get an HTTP response of a trace

http://{Jaeger_UI_IP}:16686/trace/{trace_id}
- E.g., http://localhost:16686/trace/10e2720debbab296

#### Get the trace in the JSON format

http://{Jaeger_UI_IP}:16686/api/traces/{trace_id}
- E.g., http://localhost:16686/api/traces/10e2720debbab296

### Get all traces during the last specified duration

curl -s 'http://localhost:16686/api/traces?service=nginx-web-server&lookback=50m&prettyPrint=true&limit=100'
- `service={service_name}`
- `lookback={look_back_time}`
- `prettyPrint={true_for_formatted_JSON}`
- `limit={max_num_of_traces}`

Another example:

http://localhost:16686/api/traces?end=1615178645442000&limit=20&lookback=1h&maxDuration&minDuration&operation=ReadHomeTimeline&service=nginx-web-server&start=1615175045442000

### Get search results in an HTTP response

http://localhost:16686/search?end=1615178645442000&limit=20&lookback=1h&maxDuration&minDuration&operation=ReadHomeTimeline&service=nginx-web-server&start=1615175045442000
