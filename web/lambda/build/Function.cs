using Amazon.Lambda.Core;
using Newtonsoft.Json;
using System.Net;
using System.Text.Json.Serialization;
using Amazon.Lambda.APIGatewayEvents;
using Newtonsoft.Json.Serialization;


// Assembly attribute to enable the Lambda function's JSON input to be converted into a .NET class.
//[assembly: LambdaSerializer(typeof(Amazon.Lambda.Serialization.SystemTextJson.DefaultLambdaJsonSerializer))]
[assembly: LambdaSerializerAttribute(typeof(Amazon.Lambda.Serialization.Json.JsonSerializer))]
namespace WaniCTF_Lambda;



public class Function
{

  /// <summary>
  /// A simple function that takes a string and does a ToUpper
  /// </summary>
  /// <param name="input"></param>
  /// <param name="context"></param>
  /// <returns></returns>

  public APIGatewayProxyResponse LoginWani(APIGatewayProxyRequest input, ILambdaContext context)
  {
    var parameters = input.QueryStringParameters;
    var headers = new Dictionary<string, string>()
    {
        ["Access-Control-Allow-Origin"] = "https://lambda-web.wanictf.org",
        ["Access-Control-Allow-Methods"] = "GET OPTIONS"
    };
if (parameters == null) {
      return new APIGatewayProxyResponse
      {
        StatusCode = (int)HttpStatusCode.InternalServerError,
        Body = "QueryStringParameters is null",
        Headers = headers
      };
    }
    if (!parameters.ContainsKey("UserName") || !parameters.ContainsKey("PassWord")) {
      return new APIGatewayProxyResponse
      {
        StatusCode = (int)HttpStatusCode.BadRequest,
        Body = "ユーザー名とパスワードを指定してください",
        Headers = headers
      };
    }
    var name = parameters["UserName"];
    var password = parameters["PassWord"];
    if (name == "LambdaWaniwani" && password == "aflkajflalkalbnjlsrkaerl")
    {
      return new APIGatewayProxyResponse
      {
        StatusCode = (int)HttpStatusCode.OK,
        Body = "FLAG{l4mabd4_1s_s3rverl3ss_s3rv1c3}",
        Headers = headers
      };
    }
    return new APIGatewayProxyResponse
    {
      StatusCode = (int)HttpStatusCode.OK,
      Body = $"Password or UserName are incorrect!!! :  {name}: {password}",
      Headers = headers
    };
  }


}

