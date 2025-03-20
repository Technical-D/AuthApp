from flask import jsonify

# Error handler for rate-limited requests (429 status code)
def handle_ratelimit_error(app):
    @app.errorhandler(429)
    def ratelimit_error(e):
        return jsonify({
            "error": "Too Many Requests",
            "message": "You have exceeded the number of allowed OTP requests. Please try again later."
        }), 429
