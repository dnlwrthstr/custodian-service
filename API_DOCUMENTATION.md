# API Documentation for Custodian Service

This document provides information on how to access and use the API documentation for the Custodian Service.

## Available Documentation Formats

The Custodian Service API provides documentation in multiple formats:

1. **Swagger UI**: Interactive documentation available at `/docs`
2. **ReDoc**: Alternative documentation UI available at `/redoc`
3. **OpenAPI JSON**: Raw OpenAPI specification available at `/openapi.json`

## Using API Documentation in a Frontend Project

### Option 1: Link to the API Documentation

The simplest approach is to link to the API documentation from your frontend application:

```javascript
// Example in a React application
function ApiDocsButton() {
  return (
    <a href="http://your-api-server/docs" target="_blank" rel="noopener noreferrer">
      API Documentation
    </a>
  );
}
```

### Option 2: Embed the API Documentation

You can embed the Swagger UI or ReDoc in your frontend application using an iframe:

```html
<iframe 
  src="http://your-api-server/docs" 
  width="100%" 
  height="800px" 
  title="API Documentation">
</iframe>
```

### Option 3: Generate Client Code from OpenAPI Specification

You can use the OpenAPI specification to generate client code for your frontend:

1. Download the OpenAPI specification from `/openapi.json`
2. Use tools like [OpenAPI Generator](https://openapi-generator.tech/) to generate client code:

```bash
# Install OpenAPI Generator
npm install @openapitools/openapi-generator-cli -g

# Generate TypeScript client
openapi-generator-cli generate -i openapi.json -g typescript-fetch -o ./api-client
```

3. Import and use the generated client in your frontend code:

```typescript
import { DefaultApi } from './api-client';

const api = new DefaultApi({
  basePath: 'http://your-api-server'
});

// Example: Get all custodians
async function fetchCustodians() {
  try {
    const custodians = await api.getCustodians();
    return custodians;
  } catch (error) {
    console.error('Error fetching custodians:', error);
    throw error;
  }
}
```

### Option 4: Use Swagger UI Directly in Your Frontend

You can include Swagger UI as a dependency in your frontend project:

```bash
npm install swagger-ui-react
```

Then use it in your React component:

```jsx
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';

function ApiDocumentation() {
  return <SwaggerUI url="http://your-api-server/openapi.json" />;
}
```

## Best Practices

1. **CORS Configuration**: Ensure your API server has proper CORS configuration to allow requests from your frontend application.

2. **Authentication**: If your API requires authentication, make sure to include authentication details in your documentation and client code.

3. **Versioning**: Keep track of API versions and ensure your frontend is using the correct version.

4. **Error Handling**: Implement proper error handling in your frontend when interacting with the API.

## Conclusion

Using the API documentation in your frontend project can significantly improve development efficiency and reduce integration issues. Choose the approach that best fits your project's needs and development workflow.