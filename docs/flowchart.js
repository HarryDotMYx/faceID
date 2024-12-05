// Mermaid flowchart definition
const flowchart = `
flowchart TD
    subgraph User["User Interaction"]
        A[User Login/Register] --> B[Profile Created]
        B --> C{Choose Action}
        C -->|Upload| D[Face Image Upload]
        C -->|Live| E[Live Recognition]
        C -->|Verify| F[Face Verification]
    end

    subgraph Upload["Face Image Processing"]
        D --> G[Validate Image]
        G --> H[Process Face]
        H --> I[Generate Encodings]
        I --> J[Store in Database]
    end

    subgraph Live["Live Recognition Flow"]
        E --> K[Initialize Camera]
        K --> L[Start Video Stream]
        L --> M[Capture Frame]
        M --> N[Process Frame]
        N --> O[Match Faces]
        O --> P[Render Results]
        P --> |Next Frame| M
    end

    subgraph Verify["Face Verification"]
        F --> Q[Capture/Upload Image]
        Q --> R[Process Face]
        R --> S[Compare Encodings]
        S --> T[Show Result]
    end

    subgraph Backend["Server Processing"]
        U[Frame Processing]
        V[Face Detection]
        W[Face Encoding]
        X[Face Matching]
        Y[Result Generation]
        
        U --> V
        V --> W
        W --> X
        X --> Y
    end

    subgraph Storage["Data Management"]
        Z[Media Storage]
        AA[Face Encodings]
        AB[User Profiles]
        AC[Temp Files]
        
        Z --> |Cleanup| AC
        AA --> |Update| AB
    end

    N --> U
    H --> V
    R --> V
    Y --> P
    Y --> T
    J --> AA

    style User fill:#f9f,stroke:#333,stroke-width:2px
    style Upload fill:#bbf,stroke:#333,stroke-width:2px
    style Live fill:#bfb,stroke:#333,stroke-width:2px
    style Verify fill:#fbf,stroke:#333,stroke-width:2px
    style Backend fill:#fbb,stroke:#333,stroke-width:2px
    style Storage fill:#bff,stroke:#333,stroke-width:2px
`;

// Export flowchart
module.exports = flowchart;