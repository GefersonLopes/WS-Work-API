from app import create_app;

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config.get("PORT", 3000), debug=(app.config.get("NODE_ENV")!="production"))

if app.config.get("RUN_SEED"):
    with app.app_context():
        from app.database.seed import run_seed
        run_seed()

