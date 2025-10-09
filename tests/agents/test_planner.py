"""
Tests para el Agente Planificador.

Este módulo contiene las pruebas unitarias para el agente planificador
que convierte solicitudes en lenguaje natural a planes técnicos estructurados.

Siguiendo TDD, estos tests se escriben ANTES de implementar el agente.
"""

import json
import pytest
from unittest.mock import Mock, patch
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import JsonOutputParser

# Importación del módulo implementado
from agents.planner import get_planner_chain


class TestPlannerAgent:
    """
    Tests principales para el Agente Planificador.
    """

    def test_creates_plan_from_simple_request(self):
        """
        Test que verifica la creación de un plan desde una solicitud simple.
        """
        # Arrange: Solicitud simple
        request_data = {
            "request": "Crear un programa COBOL que muestre 'HOLA MUNDO'"
        }
        
        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(request_data)
        
        # Assert: Debe retornar un plan válido
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)
        assert len(result["steps"]) > 0

    def test_creates_correction_plan_from_error(self):
        """
        Test que verifica la creación de un plan de corrección desde un error.
        """
        # Arrange: Datos de corrección
        correction_data = {
            "request": "Corregir error de sintaxis",
            "code": "IDENTIFICATION DIVISION.\nPROGRAM-ID. TEST.\nPROCEDURE DIVISION.\nDISPLAY 'ERROR'.\nSTOP RUN",
            "error_message": "Missing DATA DIVISION"
        }
        
        # Act: Generar plan de corrección
        chain = get_planner_chain()
        result = chain.invoke(correction_data)
        
        # Assert: Debe retornar un plan de corrección válido
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result
        assert "steps" in result
        assert "mode" in result
        assert result["mode"] == "correction"

    def test_handles_complex_request(self):
        """
        Test que verifica el manejo de solicitudes complejas.
        """
        # Arrange: Solicitud compleja
        complex_request = {
            "request": "Crear un programa COBOL para procesar archivos de empleados con validaciones de datos, cálculos de nómina y generación de reportes"
        }
        
        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(complex_request)
        
        # Assert: Debe manejar la complejidad
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result
        assert "steps" in result
        assert len(result["steps"]) >= 3  # Solicitud compleja debe tener múltiples pasos

    def test_validates_json_output_format(self):
        """
        Test que verifica que la salida sea JSON válido.
        """
        # Arrange: Solicitud estándar
        request_data = {
            "request": "Crear programa de validación de datos"
        }
        
        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(request_data)
        
        # Assert: Debe ser JSON válido
        assert result is not None
        assert isinstance(result, dict)
        # Verificar que se puede serializar a JSON
        json_str = json.dumps(result)
        assert json_str is not None
        # Verificar que se puede deserializar
        parsed = json.loads(json_str)
        assert parsed == result

    def test_handles_empty_request(self):
        """
        Test que verifica el manejo de solicitudes vacías.
        """
        # Arrange: Solicitud vacía
        empty_request = {"request": ""}
        
        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(empty_request)
        
        # Assert: Debe manejar graciosamente
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result or "error" in result


class TestPlannerModes:
    """
    Tests para los diferentes modos del planificador.
    """

    def test_creation_mode_structure(self):
        """
        Test que verifica la estructura del modo creación.
        """
        # Arrange: Solicitud de creación
        creation_request = {
            "request": "Crear programa de cálculo de intereses"
        }
        
        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(creation_request)
        
        # Assert: Estructura de modo creación
        assert result is not None
        assert result["mode"] == "creation"
        assert "plan" in result
        assert "steps" in result
        assert isinstance(result["steps"], list)

    def test_correction_mode_structure(self):
        """
        Test que verifica la estructura del modo corrección.
        """
        # Arrange: Datos de corrección
        correction_data = {
            "request": "Corregir programa",
            "code": "PROGRAM-ID. TEST.",
            "error_message": "Syntax error"
        }
        
        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(correction_data)
        
        # Assert: Estructura de modo corrección
        assert result is not None
        assert result["mode"] == "correction"
        assert "plan" in result
        assert "steps" in result
        assert "correction_type" in result
        assert "original_error" in result

    def test_mode_detection_logic(self):
        """
        Test que verifica la lógica de detección de modos.
        """
        # Arrange & Act: Probar ambos modos
        chain = get_planner_chain()
        
        # Modo creación (solo request)
        creation_result = chain.invoke({"request": "Crear programa nuevo"})
        
        # Modo corrección (request + code + error)
        correction_result = chain.invoke({
            "request": "Corregir error",
            "code": "PROGRAM-ID. TEST.",
            "error_message": "Error de sintaxis"
        })
        
        # Assert: Detección correcta de modos
        assert creation_result["mode"] == "creation"
        assert correction_result["mode"] == "correction"


class TestPlannerConfiguration:
    """
    Tests para la configuración del planificador.
    """

    def test_uses_correct_llm_configuration(self):
        """
        Test que verifica la configuración correcta del LLM.
        """
        # Act: Obtener la cadena
        chain = get_planner_chain()
        
        # Assert: Verificar que la cadena existe y es del tipo correcto
        assert chain is not None
        assert hasattr(chain, 'invoke')

    def test_uses_json_output_parser(self):
        """
        Test que verifica el uso del JsonOutputParser.
        """
        # Act: Generar plan y verificar formato
        chain = get_planner_chain()
        result = chain.invoke({"request": "Test parser"})
        
        # Assert: Debe ser JSON válido (dict)
        assert isinstance(result, dict)

    def test_chain_structure(self):
        """
        Test que verifica la estructura de la cadena de LangChain.
        """
        # Act: Obtener cadena
        chain = get_planner_chain()
        
        # Assert: Verificar que es una cadena ejecutable
        assert chain is not None
        assert callable(getattr(chain, 'invoke', None))


class TestPlannerEdgeCases:
    """
    Tests para casos extremos del planificador.
    """

    def test_handles_very_long_request(self):
        """
        Test que verifica el manejo de solicitudes muy largas.
        """
        # Arrange: Solicitud muy larga
        long_request = {
            "request": "Crear un sistema complejo de gestión empresarial en COBOL que incluya módulos de contabilidad, recursos humanos, inventario, ventas, compras, reportes financieros, auditoría, control de acceso, backup automático, integración con sistemas externos, validación de datos en tiempo real, procesamiento por lotes, interfaz de usuario, documentación automática, logs de sistema, manejo de errores, optimización de performance, escalabilidad horizontal, compatibilidad con mainframes legacy, migración de datos, testing automatizado, deployment continuo, monitoreo de sistema, alertas automáticas, dashboard ejecutivo, análisis predictivo, machine learning integration, API REST, microservicios, containerización, orquestación, service mesh, observabilidad, métricas de negocio, compliance regulatorio, seguridad avanzada, encriptación, autenticación multifactor, autorización granular, audit trail completo, disaster recovery, alta disponibilidad, balanceador de carga, cache distribuido, base de datos distribuida, replicación de datos, particionamiento, indexación optimizada, queries complejas, stored procedures, triggers, views, funciones personalizadas, tipos de datos custom, validaciones de integridad referencial, transacciones ACID, isolation levels, deadlock detection, connection pooling, prepared statements, batch processing, streaming de datos, ETL processes, data warehousing, business intelligence, OLAP cubes, data mining, statistical analysis, reporting engine, dashboard interactivo, visualizaciones avanzadas, export a múltiples formatos, scheduling de tareas, workflow engine, business process management, rule engine, decision trees, expert systems, knowledge base, semantic search, natural language processing, text analytics, sentiment analysis, image processing, OCR, barcode scanning, RFID integration, IoT connectivity, sensor data processing, real-time analytics, event sourcing, CQRS pattern, domain driven design, hexagonal architecture, clean architecture, SOLID principles, design patterns, refactoring tools, code quality metrics, technical debt analysis, performance profiling, memory optimization, CPU optimization, I/O optimization, network optimization, database optimization, query optimization, index tuning, partitioning strategies, archiving policies, data retention, GDPR compliance, privacy by design, data anonymization, pseudonymization, consent management, right to be forgotten, data portability, breach notification, risk assessment, vulnerability scanning, penetration testing, security audits, compliance reporting, regulatory updates, change management, version control, branching strategies, merge conflicts resolution, code reviews, pull requests, continuous integration, continuous deployment, infrastructure as code, configuration management, secrets management, environment promotion, blue-green deployment, canary releases, feature flags, A/B testing, chaos engineering, fault injection, circuit breakers, bulkhead pattern, timeout handling, retry mechanisms, exponential backoff, rate limiting, throttling, load shedding, graceful degradation, health checks, readiness probes, liveness probes, metrics collection, distributed tracing, log aggregation, alerting rules, runbooks, incident response, post-mortem analysis, root cause analysis, corrective actions, preventive measures, continuous improvement, lessons learned, knowledge sharing, documentation standards, API documentation, user manuals, training materials, onboarding guides, troubleshooting guides, FAQ sections, community forums, support tickets, escalation procedures, SLA monitoring, customer satisfaction surveys, feedback loops, product roadmap, feature prioritization, stakeholder management, project planning, resource allocation, budget tracking, cost optimization, ROI analysis, business case development, market research, competitive analysis, user research, usability testing, accessibility compliance, internationalization, localization, multi-tenancy, white-labeling, customization framework, plugin architecture, extension points, third-party integrations, marketplace ecosystem, developer portal, SDK development, API versioning, backward compatibility, deprecation policies, migration guides, upgrade procedures, rollback strategies, data migration tools, schema evolution, database migrations, index management, statistics updates, maintenance windows, capacity planning, performance benchmarking, load testing, stress testing, endurance testing, scalability testing, security testing, compatibility testing, regression testing, acceptance testing, user acceptance testing, integration testing, unit testing, test automation, test data management, test environment management, mock services, test doubles, behavior driven development, specification by example, living documentation, executable specifications, acceptance criteria, definition of done, quality gates, code coverage, mutation testing, property-based testing, contract testing, end-to-end testing, visual regression testing, accessibility testing, performance testing, security testing, compliance testing, exploratory testing, usability testing, A/B testing, multivariate testing, feature toggles, experimentation platform, analytics integration, conversion tracking, funnel analysis, cohort analysis, retention analysis, churn prediction, lifetime value calculation, segmentation strategies, personalization engine, recommendation systems, content management, digital asset management, workflow automation, approval processes, notification systems, communication channels, collaboration tools, project management integration, time tracking, resource planning, skill matrix, competency framework, performance evaluation, goal setting, OKRs, KPIs, balanced scorecard, executive dashboards, operational dashboards, real-time monitoring, predictive analytics, prescriptive analytics, machine learning models, artificial intelligence, natural language generation, automated reporting, intelligent alerts, anomaly detection, pattern recognition, trend analysis, forecasting models, simulation engines, optimization algorithms, decision support systems, expert advisory, knowledge graphs, ontologies, semantic web, linked data, data lakes, data mesh, data fabric, data governance, data lineage, data catalog, metadata management, master data management, reference data management, data quality assessment, data profiling, data cleansing, data enrichment, data transformation, data integration, data synchronization, data federation, data virtualization, data as a service, API economy, platform economy, ecosystem orchestration, partner management, supplier management, vendor management, contract management, procurement processes, financial planning, budgeting, forecasting, cash flow management, working capital optimization, investment analysis, risk management, compliance management, regulatory reporting, tax management, audit preparation, internal controls, segregation of duties, approval workflows, exception handling, escalation procedures, incident management, problem management, change management, release management, configuration management, asset management, license management, capacity management, availability management, continuity management, security management, identity management, access management, privilege management, threat management, vulnerability management, patch management, backup management, recovery management, disaster recovery, business continuity, crisis management, emergency procedures, communication plans, stakeholder notifications, media relations, public relations, brand management, reputation management, customer relations, supplier relations, investor relations, regulatory relations, community relations, environmental management, sustainability initiatives, corporate social responsibility, ethical guidelines, code of conduct, whistleblower procedures, conflict of interest policies, anti-corruption measures, fair trade practices, diversity and inclusion, equal opportunity, workplace safety, health and wellness, employee engagement, talent acquisition, talent development, succession planning, knowledge management, intellectual property management, innovation management, research and development, product development, service development, market development, business development, strategic planning, competitive intelligence, market intelligence, customer intelligence, business intelligence, operational intelligence, financial intelligence, risk intelligence, threat intelligence, security intelligence, compliance intelligence, regulatory intelligence, technology intelligence, innovation intelligence, patent intelligence, trademark intelligence, copyright management, trade secret protection, confidentiality agreements, non-disclosure agreements, licensing agreements, partnership agreements, joint venture agreements, merger and acquisition support, due diligence processes, valuation methodologies, financial modeling, scenario planning, sensitivity analysis, Monte Carlo simulation, real options valuation, discounted cash flow analysis, net present value calculation, internal rate of return, payback period analysis, break-even analysis, cost-benefit analysis, total cost of ownership, return on investment, economic value added, balanced scorecard implementation, performance measurement, benchmarking studies, best practice identification, process improvement, lean methodologies, six sigma implementation, total quality management, continuous improvement culture, innovation culture, learning organization, knowledge sharing platforms, communities of practice, center of excellence, shared services, outsourcing strategies, offshoring considerations, nearshoring options, insourcing decisions, make vs buy analysis, build vs buy decisions, technology selection, vendor evaluation, RFP processes, contract negotiations, service level agreements, key performance indicators, operational level agreements, underpinning contracts, supplier scorecards, vendor management, relationship management, partnership development, ecosystem orchestration, platform strategies, network effects, multi-sided markets, digital transformation, automation strategies, robotics process automation, artificial intelligence integration, machine learning implementation, deep learning applications, neural networks, computer vision, natural language processing, speech recognition, chatbots, virtual assistants, augmented reality, virtual reality, mixed reality, blockchain technology, distributed ledger, smart contracts, cryptocurrency integration, tokenization, decentralized finance, web3 technologies, metaverse applications, quantum computing readiness, edge computing, fog computing, cloud computing, hybrid cloud, multi-cloud strategies, serverless computing, containerization, microservices architecture, service mesh, API gateway, event-driven architecture, reactive systems, streaming architectures, lambda architecture, kappa architecture, data mesh architecture, modern data stack, cloud-native development, DevOps practices, GitOps workflows, infrastructure as code, policy as code, security as code, compliance as code, everything as code, shift-left security, shift-left testing, continuous security, continuous compliance, continuous monitoring, continuous improvement, continuous learning, continuous adaptation, continuous evolution, future-proofing strategies, technology roadmaps, digital strategies, innovation strategies, transformation strategies, growth strategies, sustainability strategies, resilience strategies, adaptability frameworks, agility frameworks, scalability frameworks, reliability frameworks, security frameworks, compliance frameworks, governance frameworks, risk frameworks, quality frameworks, performance frameworks, measurement frameworks, improvement frameworks, learning frameworks, development frameworks, deployment frameworks, operational frameworks, support frameworks, maintenance frameworks, evolution frameworks, retirement frameworks, legacy modernization, technical debt management, architecture evolution, system integration, data integration, process integration, organizational integration, cultural integration, change management, transformation management, program management, portfolio management, project management, product management, service management, relationship management, stakeholder management, communication management, knowledge management, risk management, quality management, performance management, resource management, financial management, strategic management, operational management, tactical management, crisis management, emergency management, business continuity management, disaster recovery management, security management, compliance management, governance management, audit management, control management, monitoring management, reporting management, analytics management, intelligence management, insight management, decision management, action management, execution management, delivery management, value management, benefit management, outcome management, impact management, success management, excellence management, innovation management, improvement management, optimization management, transformation management, evolution management, adaptation management, resilience management, sustainability management, responsibility management, accountability management, transparency management, integrity management, ethics management, trust management, reputation management, brand management, customer management, market management, competitive management, strategic management, operational management, financial management, human resource management, technology management, information management, knowledge management, intellectual property management, asset management, resource management, capacity management, demand management, supply management, vendor management, partner management, alliance management, ecosystem management, platform management, network management, community management, relationship management, engagement management, experience management, satisfaction management, loyalty management, retention management, acquisition management, development management, growth management, expansion management, diversification management, innovation management, disruption management, transformation management, evolution management, adaptation management, change management, transition management, migration management, integration management, consolidation management, optimization management, rationalization management, standardization management, harmonization management, synchronization management, coordination management, collaboration management, cooperation management, partnership management, alliance management, ecosystem management, network management, platform management, marketplace management, community management, social management, environmental management, governance management, compliance management, regulatory management, legal management, ethical management, responsible management, sustainable management, resilient management, adaptive management, agile management, lean management, efficient management, effective management, productive management, profitable management, valuable management, beneficial management, impactful management, successful management, excellent management, world-class management, best-in-class management, industry-leading management, market-leading management, innovative management, transformative management, evolutionary management, revolutionary management, disruptive management, pioneering management, cutting-edge management, state-of-the-art management, next-generation management, future-ready management, future-proof management, forward-thinking management, visionary management, strategic management, tactical management, operational management, execution management, delivery management, results management, outcome management, impact management, value management, benefit management, success management, excellence management, leadership management, governance management, stewardship management, custodianship management, ownership management, accountability management, responsibility management, transparency management, integrity management, ethics management, trust management, credibility management, reliability management, dependability management, consistency management, predictability management, stability management, security management, safety management, quality management, performance management, efficiency management, effectiveness management, productivity management, profitability management, sustainability management, scalability management, flexibility management, adaptability management, agility management, responsiveness management, resilience management, robustness management, durability management, longevity management, continuity management, persistence management, endurance management, strength management, power management, capability management, competency management, expertise management, mastery management, excellence management, superiority management, leadership management, dominance management, competitive advantage management, differentiation management, uniqueness management, distinctiveness management, specialization management, focus management, concentration management, alignment management, integration management, coordination management, synchronization management, harmonization management, optimization management, maximization management, enhancement management, improvement management, advancement management, progress management, development management, growth management, expansion management, evolution management, transformation management, innovation management, creativity management, invention management, discovery management, exploration management, experimentation management, learning management, knowledge management, wisdom management, intelligence management, insight management, understanding management, comprehension management, awareness management, consciousness management, mindfulness management, attention management, focus management, concentration management, dedication management, commitment management, engagement management, involvement management, participation management, contribution management, collaboration management, cooperation management, partnership management, teamwork management, unity management, solidarity management, community management, society management, civilization management, humanity management, world management, universe management, cosmos management, infinity management, eternity management, immortality management, transcendence management, enlightenment management, awakening management, realization management, actualization management, fulfillment management, completion management, perfection management, ultimate management, absolute management, infinite management, eternal management, divine management, sacred management, holy management, blessed management, miraculous management, magical management, mystical management, spiritual management, soulful management, heartful management, mindful management, conscious management, aware management, enlightened management, awakened management, realized management, actualized management, fulfilled management, complete management, perfect management, ultimate management, absolute management, infinite management, eternal management, divine management"
        }
        
        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(long_request)
        
        # Assert: Debe manejar solicitudes largas
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result or "error" in result

    def test_handles_special_characters_in_request(self):
        """
        Test que verifica el manejo de caracteres especiales.
        """
        # Arrange: Solicitud con caracteres especiales
        special_request = {
            "request": "Crear programa con símbolos: @#$%^&*()[]{}|\\:;\"'<>,.?/~`±§¿¡€£¥₹₽₩₪₫₱₡₵₦₨₹₽₩₪₫₱₡₵₦₨"
        }
        
        # Act: Generar plan
        chain = get_planner_chain()
        result = chain.invoke(special_request)
        
        # Assert: Debe manejar caracteres especiales
        assert result is not None
        assert isinstance(result, dict)
        assert "plan" in result or "error" in result

    def test_consistent_output_format(self):
        """
        Test que verifica la consistencia del formato de salida.
        """
        # Arrange: Múltiples solicitudes
        requests = [
            {"request": "Programa simple"},
            {"request": "Programa complejo con múltiples módulos"},
            {"request": "Corrección de errores", "code": "TEST", "error_message": "Error"}
        ]
        
        # Act & Assert: Verificar consistencia
        chain = get_planner_chain()
        for req in requests:
            result = chain.invoke(req)
            assert result is not None
            assert isinstance(result, dict)
            assert "plan" in result or "error" in result
            if "plan" in result:
                assert "mode" in result
                assert "steps" in result