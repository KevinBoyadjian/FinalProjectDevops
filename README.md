# FinalProjectDevops
Live scores website for European Soccer  (English Premier League, Liga Spain, Serie A Italy, French Ligue1) - DevOps Final Project
## Contributors
- Ilya


graph TD
    %% Global Entry Point
    User((User)) -->|HTTPS| R53[Route 53 DNS]
    R53 --> CF[CloudFront CDN]
    
    %% Security Layer
    subgraph Security_Edge [Edge Security]
        CF --- WAF[AWS WAF Security]
    end

    %% Secret Handshake
    CF -->|X-Custom-Header| ALB[Application Load Balancer]

    %% VPC Infrastructure
    subgraph AWS_VPC [AWS VPC - us-east-1]
        subgraph Public_Subnet [Public Subnet]
            ALB
        end

        subgraph Private_Subnet [Private Subnet]
            ALB --> EKS[EKS Cluster]
            
            subgraph EKS_Nodes [Managed Node Groups]
                Pods[App Pods - Python/Flask]
                Controllers[ALB Controller & ExternalDNS]
                Monitoring[Prometheus & Grafana]
            end
        end
    end

    %% External Data
    Pods -->|REST API| API((External Football API))

    %% Documentation Links (Optional styling)
    style Security_Edge fill:#f96,stroke:#333,stroke-width:2px
    style EKS fill:#326ce5,color:#fff
    style WAF fill:#ff4f8b,color:#fff
    style CF fill:#ff9900,color:#fff
