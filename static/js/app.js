var app = angular.module("testapp", []);

app.controller("GreetingsController", ["$http", function($http) {

	this.greetings = [];

	this.message = "";
	this.author = "";

	var that = this;

	$http.get("/_ah/api/helloworld/v1/hellogreeting").success(function(data) {
		that.greetings = data["items"];
	});

	this.generateJwtString = function(message, author) {
		var jwt_header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9";
		var encoded_message = btoa(JSON.stringify({"message": message, "name": author}))
		var hash = CryptoJS.HmacSHA256(jwt_header + '.' + encoded_message, "secret");
  		var hashInBase64 = CryptoJS.enc.Base64.stringify(hash);
  		var jwt_string = jwt_header + '.' + encoded_message + '.' + hashInBase64;
  		return jwt_string;
	};

	this.addAuthedGreeting = function() {
		var jwt_string = this.generateJwtString(this.message, this.author);
		$http({
			method: "POST",
			url: "/_ah/api/helloworld/v1/hellogreeting/authed",
			headers: {"Authorization": "Bearer " + jwt_string}
		}).success(that.callback);
	};

	this.callback = function(data) {
		if (!that.greetings) that.greetings = [];
		that.greetings.push(data);
		that.message = "";
		that.author = "";
	};

}]);
