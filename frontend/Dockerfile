# build stage

# use node v16 as base image
FROM node:16-alpine as build-stage
# create an application directory
CMD mkdir /app
# set the application directory
WORKDIR /app
# copy the package.json and package-lock.json files
COPY package*.json ./
# copy the yarn.lock file
COPY yarn.lock ./
# install dependencies
RUN yarn install
# copy the project directory
COPY / ./
# build the app
RUN yarn build

# production stage

# use nginx v1.21 as base image
FROM nginx:1.21-alpine as production-stage
# copy the build from previous stage 
COPY --from=build-stage /app/dist /usr/share/nginx/html