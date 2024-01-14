# Micro - Ecommerce Project

### To run this project you only need docker and few keys from stripe and neon for payment and database respectively


1. For Database You need Postgres Free DB from Neon and insert it into env file which you can get from here - (https://console.neon.tech/projects)
2. For Stripe Payment Just get a Stripe Secret Key and get it from here- (https://dashboard.stripe.com/test/apikeys)
3. Add this two values in .env file you can get from here - (https://gist.github.com/thedevhack/08c02909e732ef93b0e6c214c9693c8b)
4. You can get the docker from here - (https://hub.docker.com/r/thedevhack/micro-ecommerce)
5. Run the Docker Build using the below command
```bash
docker run --env-file .env -p 8001:8000 --rm --name micro-ecommerce -it micro-ecommerce
```
