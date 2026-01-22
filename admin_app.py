import customtkinter as ctk
import pyrebase
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import numpy as np
import pyperclip
from tkinter import messagebox
from PIL import Image, ImageTk  # Añadido para manejo de imágenes
import textwrap

# --- CONFIGURACIÓN FIREBASE ---
config = {
    "apiKey": "AIzaSyAXR9BZ6GejBrTWBWNdsOPKAICxzz7Kbj4",
    "authDomain": "encuestas-b3d90.firebaseapp.com",
    "databaseURL": "https://encuestas-b3d90-default-rtdb.firebaseio.com",
    "storageBucket": "encuestas-b3d90.firebasestorage.app"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# --- MATRIZ DE INTERPRETACIÓN INTEGRAL (CONTENIDO LITERAL DEL EXCEL) ---
MATRIZ_EXCEL = {
    1: {
        1: {"causa": "No hay documento aprobado ni formalizado.", "recom": "Dependencia al  fundador o gerente para entender y ejecutar la estrategia. Descoordinación en la toma de decisiones estratégicas.", "alcance": "Diagnóstico estratégico: Revisión de información existente, entrevistas con alta dirección y análisis del contexto interno y externo. Formalización del plan estratégico: Construcción del plan con objetivos, prioridades, indicadores y responsables; validación y aprobación con gerencia. Comunicación estratégica: Diseño y ejecución de un plan de comunicación para líderes y equipos, incluyendo talleres de alineación y gestión de resistencia. Alineación del talento: Implementación de piloto para calidad la traducción de la estrategia a roles, responsabilidades, planes de trabajo y mecanismos de seguimiento. Transferencia y sostenibilidad: Instalación de capacidades internas para seguimiento, toma de decisiones basada en datos y continuidad estratégica y generar ajustes.."},
        2: {"causa": "Hay un plan escrito, pero desactualizado, o solo se comunica a algunos equipos, o niveles. ", "recom": "Decisiones basadas en información parcial o desactualizada Riesgo de perder oportunidades frente a competidores.", "alcance": "Revisión del plan existente: Evaluación de vigencia, coherencia y alineación con el entorno y prioridades actuales. Ajuste estratégico con líderes: Actualización de objetivos, prioridades e indicadores clave. Cierre de brechas de comunicación: Diseño de un plan táctico para asegurar comprensión transversal. Acompañamiento a la ejecución: Implementación piloto de integración del plan en decisiones de talento, planes operativos y asignación de recursos. Seguimiento y ajustes: Ajustes del plan piloto. "},
        3: {"causa": "Hay un plan escrito, aprobado, actualizado y comunicado a todos los colaboradores.", "recom": "1. Alto nivel de comprensión y compromiso del talento. Decisiones alineadas y ejecución coherente. Mayor probabilidad de logro de resultados estratégicos..", "alcance": "Evaluación de adopción: Análisis del uso real del plan en decisiones, prioridades y asignación de recursos. Refuerzo de prácticas efectivas: Ajustes focalizados para maximizar impacto. Transferir y desarrollar líderes: Formación de líderes responsables sobre la planeación estratégica y su sostenibilidad. Mejora continua: Instalación de mecanismos de retroalimentación e innovación estratégica.ard."}
    },
    2: {
        1: {"causa": "Los líderes no asignan presupuesto, personas y tiempo con criterios estratégicos definidos; lo asignan de acuerdo a urgencias o decisiones reactivas.", "recom": "Proyectos o actividades sin recursos asignados.Recursos desperdiciados en actividades que no generan impacto en resultados.", "alcance": "Diagnóstico de asignación actual de recursos. Definición de prioridades estratégicas y criterios de asignación. Comunicación y alineación con líderes. Implementación piloto para evaluar vinculación de recursos a responsables y planes de trabajo. Transferir el uso de seguimiento y control y hacer ajustes. "},
        2: {"causa": "Parte del presupuesto, personal y tiempo se asigna según prioridades estratégicas, pero hay inconsistencias entre áreas y líderes.", "recom": "Algunos proyectos estratégicos avanzan, otros se retrasan. Desalineación parcial entre objetivos y ejecución y esfuerzos de equipo fragmentados.", "alcance": "Revisión del uso actual de recursos: Analizar cómo se asignan los recursos actualmente frente a las prioridades estratégicas y detectar inconsistencias o desviaciones por área. Diseño de criterios comunes en la asignación de recursos: Construcción de criterios claros y compartidos para asignar recursos. Ajuste de prioridades y asignación de recursos: Alinear objetivos estratégicos con recursos disponibles, definiendo reglas claras de asignación que reduzcan discrepancias.Alineación y capacitación de líderes: Socializar criterios de asignación con todos los líderes responsables y generar talleres para asegurar comprensión y compromiso. Implementación controlada piloto: Aplicar los criterios de asignación en áreas críticas, monitorear y ajustar resultados. Seguimiento y cierre de brechas: Revisión y ajustes de acuerdo a piloto. "},
        3: {"causa": "Las decisiones de asignación de presupuesto, personas y tiempo siguen consistentemente el plan estratégico en todos los niveles de la organización.", "recom": "Optimización de recursos. Maximización de impacto en resultados de negocio.", "alcance": "Evaluar adopción y efectividad: Identificar oportunidades de optimización.. Ajustar y alinear: Ajuste de criterios de priorización. Diseño de un modelo de gobernanza para decisiones de asignación, Claridad de roles, comités y mecanismos de escalamiento y reglas claras para repriorización frente a cambios del entorno. Transferir y formar líderes: Fortalecimiento de capacidades de líderes en toma de decisiones complejas. Innovación continua: Establecer mecanismos de retroalimentación y mejora continua en la asignación de recursos."}
    },
    3: {
        1: {"causa": "La organización no traduce la estrategia en planes de trabajo concretos, medibles y ejecutables. La estrategia no se convierte en acciones operativas", "recom": "Estrategia sin ejecución tangible. Confusión sobre responsabilidades y prioridades. Alto riesgo de proyectos incompletos o duplicados.", "alcance": "Diagnóstico de ejecución estratégica: Mapa de brechas entre estrategia y ejecución operativa. Diseño del modelo de planificación operativa: Definir un modelo estándar de planificación operativa alineada a la estrategia. Construcción de planes operativos: Acompañar a líderes en la construcción de sus planes operativos. (piloto). Comunicación y alineación organizacional: Diseñar e implementar un plan de comunicación de los planes operativos, facilitar talleres de alineación para gestionar resistencia al cambio. Seguimiento, control y sostenibilidad: Transferir capacidades a líderes para asegurar continuidad sin dependencia, instalación de capacidades internas."},
        2: {"causa": "Existen planes operativos, pero su cobertura parcial genera desigualdad en ejecución y resultados inconsistentes.", "recom": "Duplicación de esfuerzos. Resultados inconsistentes. Fricción interna por prioridades contradictorias.", "alcance": "Diagnóstico de consistencia operativo: Revisar los planes operativos existentes por área, identificar brechas entre áreas con y sin planes operativos Definición de estándares comunes: Ajustar el modelo existente para que sea aplicable a toda la organización y validar el modelo, Alineación y ajuste de planes por área: Acompañar a las áreas con planes parciales para que se realicen ajustes y alineación entre áreas. Comunicación e implementación controlada piloto: Comunicar el modelo operativo común a líderes y equipos y adopción del modelo operativo común en todas las áreas intervenidas. Seguimiento y cierre de brechas: Implementar rutinas de seguimiento homogéneas, revisión y ajustes de acuerdo a piloto, ajustar desviaciones y cerrar brechas detectadas. "},
        3: {"causa": "La estrategia se traduce en acciones concretas en toda la organización, con criterios comunes de ejecución, seguimiento y responsabilidad en todos los niveles.", "recom": "Ejecución uniforme y eficiente. Claridad en roles, responsabilidades y prioridades.", "alcance": "Evaluación de efectividad de la ejecución: Evaluar la calidad de los planes operativos (no solo su existencia) y diagnosticar efectividad de la ejecución estratégica. Optimizar prioridades y foco: Ajustar planes operativos para maximizar impacto en resultados clave Fortalecimiento de la gobernanza de ejecución: Modelo de gobernanza de la ejecución estratégica. Desarrollo de capacidades de liderazgo para la ejecución: Transferir prácticas de alto desempeño a los equipos. Innovación y mejora continua: Instalar mecanismos de retroalimentación continua. Resultados esperados: Ejecución estratégica de alto desempeño y sostenible."}
    },
    4: {
        1: {"causa": "No existen mecanismos formales de coordinación. Las interacciones dependen de relaciones informales, personas clave o improvisación, lo que impide una ejecución coordinada de la estrategia.", "recom": "Equipos desalineados y trabajos en silos. Duplicación de esfuerzos y desperdicio de recursos. Decisiones inconsistentes entre áreas.", "alcance": "Diagnóstico estructural: análisis de estructura actual, flujos reales de trabajo y puntos de fricción. Diseño de interacciones clave: definición de cómo deben coordinarse áreas y roles críticos para ejecutar la estrategia. Formalización de flujos y gobernanza: reglas de coordinación, toma de decisiones y escalamiento. Alineación con talento: ajuste de roles, responsabilidades y capacidades requeridas. Transferencia y adopción: acompañamiento a líderes para asegurar uso efectivo de la estructura."},
        2: {"causa": "Existen reglas de coordinación formales en ciertas áreas, pero no de manera transversal. La ejecución depende del criterio de cada área o líder.", "recom": "Riesgo de conflictos por decisiones contradictorias. Mensajes inconsistentes al equipo. Baja optimización de recursos compartidos.", "alcance": "Mapeo de interacciones parciales: identificar dónde funcionan y dónde fallan. Definición de estándares de coordinación: reglas comunes de interacción entre áreas y roles. Ajuste estructural focalizado: correcciones sin rediseño total. Alineación de líderes: criterios comunes para decisiones inter-áreas. Seguimiento de efectividad: indicadores de coordinación y ejecución."},
        3: {"causa": "La coordinación, dependencias y flujos de decisión están formalmente definidos y se aplican de manera consistente en toda la organización.", "recom": "Coordinación entre areas y roles. Uso eficiente de recursos.", "alcance": "Evaluación de efectividad estructural. Optimización de flujos críticos de decisión. Fortalecimiento de gobernanza transversal. Desarrollo de capacidades organizacionales. Mejora continua del modelo organizacional."},
    },
    5: {
        1: {"causa": "Las responsabilidades no están definidas ni comunicadas. El trabajo se asigna según la persona o la urgencia del momento.", "recom": "Duplicidad de tareas. Conflictos por responsabilidades no claras. Alta dependencia del jefe para coordinar trabajo. ", "alcance": "Diagnóstico de roles reales vs. formales. Definición de responsabilidades y entregables. Validación con líderes. Comunicación y socialización. Integración a procesos de talento."},
        2: {"causa": "Existen definiciones formales solo para ciertos roles, sin un estándar común. La asignación del trabajo es inconsistente entre áreas.", "recom": "Confusión sobre quién debe hacerse cargos de ciertas actividades. Cargas de trabajo desiguales entre roles similares. Ejecución desigual entre áreas.", "alcance": "Identificación de brechas entre áreas. Definición de estándar común de roles. Ajuste y alineación transversal. Integración con evaluación de desempeño. Seguimiento de adopción."},
        3: {"causa": "Todos los cargos y roles cuentan con responsabilidades formales y comunicadas, asignando el trabajo con los mismos criterios en  toda la organización. ", "recom": "Reducción de duplicidad de tareas. Claridad en responsabilidades y expectativas. Mayor foco y eficiencia operativa.", "alcance": ". Evaluación de efectividad del modelo de roles:  Analizar si las responsabilidades actuales realmente habilitan la ejecución estratégica, identificar solapamientos, vacíos de responsabilidad o cuellos de botella y evaluar coherencia entre roles, indicadores, resultados y toma de decisiones. Optimización de responsabilidades y entregables: Ajustar responsabilidades para eliminar redundancias y ambigüedades, reforzar responsabilidades críticas para la estrategia, alinear entregables clave de cada rol con objetivos estratégicos y asegurar claridad en accountability y toma de decisiones. Integrar el modelo de roles a la gestión del talento: Vincular roles a procesos de desempeño, desarrollo y sucesión. modelo de roles integrado a los procesos de talento Flexibilidad y adaptación estratégica: Diseñar criterios para ajustar roles ante cambios del negocio, lineamientos de evolución y adaptación del modelo de roles. Transferencia y sostenibilidad: Capacitar a líderes en uso y gestión del modelo de roles, instalar prácticas de revisión periódica del modelo. Definir responsables de mantenimiento y actualización y asegurar uso consistente del modelo en decisiones cotidianas."}
    },
    6: {
        1: {"causa": "La gestión del talento no sigue estándares definidos ni responde a las prioridades estratégicas del negocio.", "recom": "Decisiones de talento inconsistentes. Alta dependencia de líderes para la toma de decisiones individuales.", "alcance": "Diagnóstico de procesos actuales: identificar brechas entre estrategia y gestión del talento desde la experiencia del colaborador. Diseño de procesos clave: Atracción, desempeño, desarrollo, sucesión y retención alineados a la estrategia. Definición de estándares y criterios: Reglas claras para decisiones de talento. Acompañamiento: Implementación piloto, comunicación y acompañamiento a líderes y RRHH. Transferencia y gobierno: Asegurar uso consistente y sostenibilidad."},
        2: {"causa": "Existen procesos de talento definidos, ágiles en algunas áreas sin cobertura total por lo cual la alineación del talento es parcial y no homogénea.", "recom": "Pérdida de eficiencia por falta de estandarización. Resultados desiguales entre áreas.", "alcance": "Diagnóstico de madurez de procesos de talento: Evaluar el nivel de formalización, agilidad y alineación estratégica de los procesos de talento existentes (atracción, desempeño, desarrollo, sucesión, compensación y retención). Identificar diferencias entre procesos y puntos de fricción en la experiencia de los colaboradores. Definición del modelo estándar de procesos de talento: Diseñar un modelo común de procesos de talento. El modelo considera flexibilidad operativa. Acompañar a líderes y RRHH en la comprensión y adopción del modelo estándar, asegurando que los procesos de talento guíen decisiones reales sobre personas.  Implementación piloto y ajuste operativo: Implementar los procesos estandarizados en áreas prioritarias, ajustando herramientas, flujos y responsabilidades. Seguimiento, cierre de brechas y sostenibilidad: Establecer mecanismos de seguimiento, indicadores de adopción y ajustes continuos. "},
        3: {"causa": "La organización tiene todos los procesos de talento formales, operativos y alineados a la estrategia que permite que la gestión del talento es coherente con la estrategia. ", "recom": "Consistencia en decisiones de talento. Soporte estructural a la ejecución estratégica. ", "alcance": "Evaluación de efectividad e integración del sistema de talento: Analizar cómo los procesos de talento funcionan como un sistema integrado, evaluando impacto real en la ejecución estratégica, desempeño organizacional y resultados del negocio. Optimización de procesos y toma de decisiones: Refinar procesos, criterios e indicadores para asegurar que cada decisión de talento (contratación, desarrollo, sucesión, desempeño) esté directamente conectada con prioridades estratégicas actuales y futuras. Fortalecimiento de capacidades de liderazgo en gestión del talento: Desarrollar en líderes la capacidad de usar los procesos de talento como herramientas estratégicas, no solo operativas, fortaleciendo accountability y calidad de decisiones. Gobierno del sistema de talento: Diseñar un modelo de gobierno que asegure consistencia, actualización continua y alineación permanente de los procesos de talento con la evolución estratégica del negocio. Mejora continua y escalabilidad: Instalar mecanismos de retroalimentación, innovación y mejora continua que permitan adaptar los procesos de talento a cambios del entorno, crecimiento organizacional o nuevas prioridades estratégicas."}
    },
    7: {
        1: {"causa": "La estrategia se gestiona por experiencias individuales de los líderes  o urgencias operativas.", "recom": "Deiciones reactivas o inconsistentes con los resultados de negocio. Reprocesosfrecuentes  y pérdida de foco estratégico. Incapacidad de anticipar desvíos o corregir a tiempo.", "alcance": "Diagnóstico estratégico y de decisiones: Analizar cómo se toman actualmente las decisiones estratégicas, qué información se utiliza y qué decisiones críticas carecen de datos de soporte. Diseño del modelo de indicadores estratégicos: Definir indicadores clave de avance estratégico alineados a objetivos, prioridades y resultados del negocio. Establecer definiciones, fuentes y frecuencia. Diseño de reportes estratégicos: Construir reportes claros, ejecutivos y orientados a la toma de decisiones, evitando sobrecarga de información y foco operativo. Instalación de rutinas de gestión estratégica: Definir comités, ciclos de revisión, responsables y reglas de uso de los datos para decisiones estratégicas. Acompañamiento y transferencia a líderes; Acompañar a los líderes en el uso real de indicadores y reportes, asegurando adopción, disciplina y sostenibilidad del modelo."},
        2: {"causa": "La información existe, pero carece de responsables, rutinas y criterios, por lo que no orienta consistentemente las decisiones estratégicas.", "recom": "Sesgos en la toma de decisiones. Ejecución desigual de la estrategia entre áreas o líderes. Ajustes tardíos o incompletos frente a cambios del entorno.", "alcance": "Diagnóstico del sistema de información estratégica: Revisar indicadores disponibles, reportes existentes, fuentes de datos y su vinculación real con objetivos estratégicos. Definición de responsables y rutinas de gestión: Establecer responsables claros por indicador, definir rutinas de revisión (comités, ciclos mensuales/trimestrales) y criterios mínimos para el uso de datos en la toma de decisiones. Alineación de indicadores con decisiones clave: Vincular explícitamente cada indicador estratégico con decisiones concretas (priorización, reasignación de recursos, ajustes de planes), reduciendo ambigüedad en su uso. Acompañamiento a líderes en la toma de decisiones con datos: Implementación piloto acompañando a líderes en la interpretación de reportes, uso de indicadores y aplicación práctica en decisiones reales del negocio. Seguimiento y cierre de brechas de uso: medir adopción, calidad de decisiones y consistencia entre áreas, ajustando indicadores y rutinas para asegurar uso sostenido."},
        3: {"causa": "Las decisiones se toman con datos objetivos sobre el avance de la estrategia lo cual permite generar ajustes de manera flexible de acuerdo al entorno o al contexto interno .", "recom": "Ajustes flexibles y  oportunos a la estrategia. Ventaja competitiva sostenible.", "alcance": "Evaluación de efectividad del sistema de indicadores Analizar impacto real de los indicadores en decisiones estratégicas, priorización y resultados del negocio. Optimización del portafolio de indicadores estratégicos: Ajustar indicadores para asegurar foco estratégico, simplicidad, trazabilidad y conexión directa con resultados clave. Fortalecimiento de capacidades analíticas de liderazgo; Desarrollar competencias en líderes para análisis, interpretación avanzada y toma de decisiones estratégicas basadas en datos. Gobierno de datos estratégicos: Definir reglas de actualización, calidad, uso y evolución de indicadores estratégicos alineados a la estrategia. Mejora continua y adaptación al entorno: Instalar mecanismos de revisión periódica que permitan adaptar indicadores y decisiones a cambios del negocio y del mercado."}
    },
    8: {
        1: {"causa": "Las decisiones de personas son subjetivas, reactivas y desconectadas de las prioridades estratégicas del negocio.", "recom": "Desalineación entre personas y estrategia. Rotación no deseada. Inversiones en talento con bajo retorno estratégico.", "alcance": "Diagnóstico de decisiones críticas de talento: Identificar decisiones clave (selección, desarrollo, desempeño, rotación, sucesión) y cómo se toman actualmente. Definición de indicadores estratégicos de talento: Diseñar indicadores mínimos necesarios para soportar decisiones de talento alineadas a la estrategia (desempeño, capacidades críticas, rotación clave, etc.). Diseño de reportes de talento: Construir reportes simples, claros y accionables para líderes y RRHH, conectando talento con resultados estratégicos. Instalación de rutinas de revisión de talento: Definir comités, ciclos y responsables para revisar datos de talento y tomar decisiones informadas. Acompañamiento y transferencia: Acompañar a líderes y RRHH en el uso práctico de datos de talento, asegurando adopción y consistencia."},
        2: {"causa": "La información de talento existe sin embargo la toma de decisiones y resultados es inconsistente entre áreas.", "recom": "Decisiones inconsistentes entre líderes. desarrollo desigual del talento. Dificultad para priorizar capacidades críticas para la estrategia.", "alcance": "Diagnóstico de indicadores de talento existentes: Revisar métricas actuales, calidad de datos y su conexión con prioridades estratégicas. Definir indicadores críticos de talento: Priorizar indicadores clave (desempeño, potencial, rotación, capacidades críticas) alineados a la estrategia del negocio. Alineación con líderes y RRHH: Definir criterios comunes para el uso de indicadores en decisiones de selección, desarrollo, sucesión y retención. Implementación de rutinas de revisión de talento: Instalar comités, ciclos de análisis y reportes periódicos que integren datos de talento en decisiones reales. Seguimiento y ajuste: Medir consistencia en el uso de indicadores y ajustar prácticas para asegurar adopción transversal."},
        3: {"causa": "La gestión del talento se basa en datos objetivos y consistentes, alineando decisiones de personas con las prioridades estratégicas de la organización.", "recom": "Mejor asignación y desarrollo del talento. Mayor capacidad de ejecución estratégica. Sostenibilidad de resultados y fortalecimiento del rol estratégico de RRHH.", "alcance": "Evaluación del impacto de decisiones de talento: Analizar cómo las decisiones basadas en datos influyen en resultados estratégicos y desempeño organizacional. Integración de indicadores de talento y negocio: Conectar métricas de talento con indicadores de negocio para decisiones predictivas y estratégicas. Desarrollo de capacidades analíticas en líderes y RRHH: Fortalecer competencias para análisis avanzado y uso estratégico de datos de talento. Gobierno de datos de talento: Definir estándares, calidad, confidencialidad y evolución de los indicadores de talento. Mejora continua y analítica predictiva: Instalar prácticas de análisis continuo y anticipación de riesgos y oportunidades de talento."}
    },
    9: {
        1: {"causa": "El talento no incorpora la tecnología como parte de su forma de trabajo, se percibe como un requisito operativo y no como un habilitador del desempeño.", "recom": "Subutilización de inversiones tecnológicas, fricción operativa y duplicidad de tareas. Alto riesgo de incumplimiento de objetivos estratégicos", "alcance": "Diagnóstico de uso tecnológico y brechas: Evaluar herramientas disponibles, niveles de adopción, capacidades del talento y barreras culturales u operativas. Definición de casos de uso estratégicos: Identificar procesos críticos donde la tecnología debe habilitar productividad, coordinación o toma de decisiones. Acompañamiento en adopción práctica: Acompañar a equipos clave en el uso efectivo de las herramientas, enfocándose en resultados y no solo en funcionalidades. Desarrollo de capacidades básicas: Fortalecer competencias mínimas necesarias para el uso efectivo de tecnología en el trabajo diario. Seguimiento y sostenibilidad: Monitorear adopción, resolver fricciones y asegurar que la tecnología apoye efectivamente la ejecución estratégica."},
        2: {"causa": "La ejecución depende de prácticas de los equipos y no de estándares organizacionales compartidos.", "recom": "Ineficiencias, Dificultad para escalar resultados, Pérdida de sinergias organizacionales.", "alcance": "Diagnóstico de uso y adopción tecnológica: Evaluar brechas de uso, capacidades y prácticas entre equipos. Definición de estándares de uso: Establecer criterios comunes de uso tecnológico alineados a procesos y objetivos estratégicos. Acompañamiento a equipos clave: Acompañar la adopción en equipos prioritarios, ajustando herramientas y prácticas. Capacitación aplicada: Desarrollar capacidades prácticas enfocadas en desempeño y resultados. Seguimiento de adopción y resultados: Medir impacto en productividad y coordinación."},
        3: {"causa": "La tecnología potencia productividad, coordinación y decisiones basadas en datos en toda la organización.", "recom": "Mayor productividad y agilidad organizacional. Mejor uso de datos e indicadores. Sostenibilidad de los resultados estratégicos.", "alcance": "Evaluación de impacto tecnológico en la estrategia: Analizar cómo la tecnología potencia resultados estratégicos. Optimización de herramientas y prácticas: Ajustar herramientas para maximizar adopción y valor. Desarrollo de capacidades digitales avanzadas: Levantar el plan de formación de competencias digitales alineadas a la estrategia. Gobierno tecnológico: Definir estándares, responsabilidades y evolución tecnológica. Innovación y mejora continua: Integrar nuevas tecnologías según necesidades estratégicas."}
    },
    10: {
        1: {"causa": "La organización desconoce cómo los colaboradores perciben su relación con la empresa desconociendo el impacto en compromiso, desempeño y ejecución de la estrategia. ", "recom": "Desalineación entre experiencia del colaborador y prioridades estratégicas.Riesgo de rotación de talento clave. Decisiones de talento con bajo impacto en resultados de negocio.", "alcance": "Modelo formal de medición y gestión: Implementar un modelo integral que capture momentos críticos de la experiencia del colaborador a lo largo de su ciclo de vida (onboarding, desarrollo, desempeño, feedback, retención, desvinculación). Integrar múltiples fuentes de información: encuestas, entrevistas, métricas de desempeño, engagement y feedback continuo. Establecer criterios de análisis que permitan identificar tendencias, brechas y oportunidades de mejora estratégica. Integrar la información de experiencia del colaborador con indicadores de negocio para apoyar la ejecución estratégica. Acompañamiento y capacitación avanzada: entrenar a líderes y equipos de talento en interpretación de datos complejos y toma de decisiones estratégicas. Promover cultura de análisis y acción basada en evidencia en toda la organización. Seguimiento y sostenibilidad: Crear dashboards estratégicos para monitorear impacto en desempeño, compromiso y resultados de negocio. Medir predictibilidad y sostenibilidad de resultados mediante KPIs integrados de talento y negocio. Ajustar modelo continuamente con base en datos y resultados de medición longitudinal."},
        2: {"causa": "La experiencia del colaborador se monitorea en algunos momentos y la información no se traduce en decisiones que soporten la estrategia.", "recom": "Mejores prácticas aisladas sin impacto organizacional. Experiencias inconsistentes entre áreas y equipos. Oportunidades de mejora no capitalizadas que afectan productividad y desempeño.", "alcance": "Diagnóstico de gestión y medición;: valuar cómo se mide la experiencia del colaboradores, identificando brechas. Mapear momentos críticos de experiencia (onboarding, desempeño, feedback, desvinculación, etc.)., Identificar herramientas, formatos y reportes existentes. Definición de estándares de medición: Establecer formatos estandarizados de recolección y análisis de datos, determinar criterios claros para traducir la información en decisiones estratégicas. Documentar procedimiento, Acompañamiento a equipos clave: Identificar áreas prioritarias según impacto y nivel de madurez en experiencia del colaborador, asignar líderes de proyecto para acompañar implementación de estándares. Capacitación aplicada: Diseñar talleres prácticos para líderes y equipos sobre interpretación de datos y toma de decisiones basada en evidencia. Entrenar en uso de herramientas y formatos estandarizados. Incluir simulaciones de situaciones reales para asegurar aprendizaje. Seguimiento de adopción y resultados; Establecer un tablero de control centralizado para monitorear adopción, consistencia y resultados, medir impacto en productividad, desempeño y engagement. Ajustar estrategias según resultados y aprendizajes."},
        3: {"causa": "La experiencia del colaborador se mide a lo largo del ciclo de vida y se utiliza activamente para priorizar decisiones de talento alineadas con la estrategia.", "recom": "Mayor compromiso y desempeño del talento clave. Soporte directo a la ejecución estratégica. Mayor predictibilidad y sostenibilidad de resultados.", "alcance": "Establecer un modelo de experiencia del colaborador  Diagnóstico inicial de la experiencia del colaborador: Evaluar cómo los colaboradores perciben su relación con la organización  Definición de indicadores básicos de experiencia: Identificar los momentos críticos del ciclo de vida del colaborador donde la experiencia tiene mayor impacto en desempeño y retención. Acompañamiento en uso práctico de información de experiencia: Apoyar a líderes y RRHH en la utilización de datos de experiencia de manera puntual para tomar decisiones. Desarrollo de capacidades mínimas para gestionar la experiencia: Capacitar a líderes y equipos de RRHH en la interpretación de indicadores básicos y acciones correctivas. Seguimiento y sostenibilidad inicial: Monitorear las primeras mediciones, resolver fricciones y asegurar que los datos comiencen a ser utilizados como soporte básico para decisiones de talento."}
    },
    11: {
        1: {"causa": "La organización no comunica de forma clara por qué es un lugar atractivo para trabajar, perdiendo capacidad de competir por talento clave.", "recom": "Dificultad para atraer y retener talento clave. Baja sentido de pertenencia y compromiso. Dependencia excesiva de incentivos transaccionales.", "alcance": "Establecer un modelo de experiencia del colaborador  Diagnóstico inicial de la experiencia del colaborador: Evaluar cómo los colaboradores perciben su relación con la organización  Definición de indicadores básicos de experiencia: Identificar los momentos críticos del ciclo de vida del colaborador donde la experiencia tiene mayor impacto en desempeño y retención. Acompañamiento en uso práctico de información de experiencia: Apoyar a líderes y RRHH en la utilización de datos de experiencia de manera puntual para tomar decisiones. Desarrollo de capacidades mínimas para gestionar la experiencia: Capacitar a líderes y equipos de RRHH en la interpretación de indicadores básicos y acciones correctivas. Seguimiento y sostenibilidad inicial: Monitorear las primeras mediciones, resolver fricciones y asegurar que los datos comiencen a ser utilizados como soporte básico para decisiones de talento."},
        2: {"causa": "La propuesta de valor existe, pero no se usa para generar orgullo y pertenecía a la organización. ", "recom": "Atracción y retención de talento inconsistente. Falta de diferenciación frente a competidores. Bajo impacto de la EVP en desempeño y resultados.", "alcance": "Activación de la EVP en equipos prioritarios y áreas clave. Integración de la EVP con procesos de talento, comunicación interna y marca empleadora. Medición de percepción y efecto de la EVP en compromiso y desempeño. Diagnóstico y alineación de la EVP. Activación piloto: Seleccionar áreas o equipos estratégicos para implementar la EVP como ventaja competitiva. Capacitación y comunicación aplicada. Seguimiento de impacto Medir cómo la activación de la EVP influye en compromiso, retención, desempeño y atracción de talento. Ajustar iniciativas según resultados y feedback de los colaboradores."},
        3: {"causa": "La propuesta de valor guía la atracción, desarrollo y permanencia del talento clave, alineando expectativas del colaborador con las prioridades estratégicas.", "recom": "Retención de talento crítico. Mayor posicionamiento como empleador estratégico. Ventaja competitiva difícil de replicar.", "alcance": "Escalamiento de la EVP a toda la organización de forma consistente. Integración total con procesos estratégicos de talento, marca empleadora y cultura organizacional. Medición continua y ajuste de la EVP para asegurar impacto sostenido."}
    },
    12: {
        1: {"causa": "La organización carece de información objetiva sobre cómo los comportamientos y decisiones de los líderes afectan compromiso, desempeño y resultados.", "recom": "Desarrollo de líderes basado en percepciones subjetivas. Riesgo de bajo desempeño y rotación por liderazgo inefectivo. Falta de control sobre una variable crítica de la ejecución estratégica.", "alcance": "Definir comportamientos de liderazgo críticos vinculados explícitamente a la estrategia y a resultados del negocio. Diseñar indicadores de impacto del liderazgo en: compromiso, desempeño, retención de talento clave. Establecer criterios comunes de medición y análisis, eliminando evaluaciones basadas en percepciones aisladas. Construir un marco de lectura que permita identificar riesgos de liderazgo que afectan la ejecución estratégica."},
        2: {"causa": "Existen datos, pero su uso es desigual, lo que limita la capacidad de corregir comportamientos de liderazgo que afectan la estrategia.", "recom": "Resultados dispares entre equipos y áreas. Intervenciones de desarrollo poco focalizadas. Percepción de inequidad en la gestión del liderazgo.", "alcance": "Implementar el modelo en equipos y roles prioritarios mediante pilotos controlados. Integrar datos de liderazgo con experiencia del colaborador, desempeño y retención. Priorizar 1–2 brechas críticas de liderazgo por equipo o líder, vinculadas a impactos estratégicos concretos. Diseñar intervenciones de desarrollo focalizadas, con responsables claros y seguimiento formal. Medir evolución de resultados y consistencia entre áreas."},
        3: {"causa": "Los datos sobre liderazgo permiten desarrollar competencias críticas, corregir desviaciones y fortalecer la ejecución de la estrategia.", "recom": "Liderazgo alineado y consistente con la estrategia. Mayor compromiso, desempeño y retención. Ejecución estratégica más predecible y sostenible.", "alcance": "Evaluar de manera periódica la efectividad del liderazgo y su impacto en resultados estratégicos. Ajustar competencias y comportamientos de liderazgo según la evolución del negocio. Integrar la medición del liderazgo en decisiones clave de talento, sucesión y desempeño. Transferir el modelo a líderes y equipos clave, asegurando autonomía, consistencia y replicabilidad. Establecer mecanismos de mejora continua y alertas tempranas sobre riesgos de liderazgo."}
    },
    13: {
        1: {"causa": "La organización no tiene claridad sobre qué roles y personas son indispensables para ejecutar la estrategia.", "recom": "Riesgo alto de pérdida de talento crítico sin anticipación. Impacto directo en continuidad operativa y resultados estratégicos.", "alcance": "Definir criterios formales y homogéneos para identificar cargos críticos, considerando impacto estratégico, dependencia del rol, escasez de capacidades y dificultad de reemplazo. Diferenciar explícitamente: riesgo estructural del cargo, riesgo asociado a la persona (talento clave). Alinear el modelo con la estrategia, prioridades del negocio y objetivos de resultados. Identificar todos los cargos críticos y talento clave a nivel organizacional, evitando visiones parciales o sesgadas por área. Priorizar cargos y personas críticas según nivel de riesgo e impacto en la estrategia. Definir acciones iniciales de mitigación (alertas, responsables, decisiones inmediatas) para reducir riesgos críticos identificados. Piloto: integrar el mapa de criticidad en decisiones clave de talento (asignaciones, continuidad, foco directivo). Transferir el modelo, criterios y herramientas a líderes y equipos responsables de talento. Establecer roles, responsabilidades y rutinas de actualización periódica del mapa de cargos críticos y talento clave."},
        2: {"causa": "La identificación es parcial y concentrada en ciertas áreas, sin una visión integral del negocio.", "recom": "Riesgo de decisiones de desarrollo o retención inconsistentes. Brechas de capacidad no visibles en áreas no evaluadas.", "alcance": "Activación del modelo en áreas prioritarias Implementar el modelo de identificación de cargos críticos y talento clave en áreas, procesos o proyectos de mayor impacto estratégico. Validar la aplicación homogénea de criterios y asegurar consistencia entre líderes y equipos. Priorización de riesgos y brechas críticas Analizar el mapa de cargos críticos y talento clave para identificar riesgos prioritarios de continuidad y desempeño. Priorizar un número acotado de cargos y personas críticas según impacto en resultados y nivel de riesgo. Integración en decisiones de talento Utilizar el modelo como insumo formal para decisiones de desarrollo, retención, sucesión y asignación de oportunidades. Definir responsables claros (líderes y HR) para la gestión de riesgos asociados al talento clave. Seguimiento y control Monitorear la evolución de riesgos, brechas y acciones definidas. Medir impacto en continuidad operativa, desempeño y estabilidad del talento clave. Ajustar criterios, procesos o focos según resultados observados."},
        3: {"causa": "La organización conoce todos los cargos críticos y talento clave y esto le permite tomar decisiones oportunas y proactivas para la Gestión Estratégica del talento.", "recom": "Continuidad operativa, Decisiones proactivas sobre talento alineadas a la estrategia.", "alcance": "Evaluación de efectividad del modelo,,  su adopción por líderes y su impacto en resultados estratégicos. Identificar desviaciones, subutilización o sesgos en la gestión del talento crítico. Ajuste dinámico y alineación estratégica. Actualizar criterios de criticidad y talento clave según cambios en la estrategia, estructura o modelo de negocio. Ajustar planes de desarrollo, sucesión y retención en función de nuevas prioridades estratégicas. Integración en la gobernanza del talento, integrar el modelo en procesos clave: planeación estratégica, desempeño, sucesión, inversión en talento y toma de decisiones ejecutivas. Utilizar el mapa de cargos críticos y talento clave como herramienta predictiva y no solo descriptiva. Transferencia avanzada y mejora continua; Transferir capacidades avanzadas a líderes y equipos responsables para asegurar autonomía y replicabilidad. Establecer rutinas de revisión, alertas tempranas y mecanismos de mejora continua que garanticen sostenibilidad del modelo en el tiempo."},
    },
    14: {
        1: {"causa": "La salida de personas clave se detecta tarde y no se gestiona como riesgo estratégico.", "recom": "Pérdida inesperada de talento crítico. Afectación directa a resultados y ejecución estratégica.", "alcance": "Evaluar: Mapear roles estratégicos y talento clave, priorizando aquellos con mayor impacto en resultados y proyectos críticos. Diagnosticar riesgo de fuga: Generar un mapa de riesgo de fuga del talento crítico, integrando desempeño, engagement y oportunidades de desarrollo, para priorizar acciones concretas. Diseñar planes de desarrollo y retención: Definir planes individuales que cierren brechas críticas de desempeño y reduzcan riesgos de fuga, vinculados a objetivos estratégicos. Transferir: Garantizar sostenibilidad del talento crítico mediante seguimiento continuo, responsabilidades claras y decisiones basadas en datos existentes."},
        2: {"causa": "Existen análisis o acciones aisladas, pero no cubren todos los roles críticos ni se integran a decisiones estratégicas.", "recom": "Riesgos no visibles en roles clave. Decisiones parciales de retención, sucesión y desarrollo.", "alcance": "Consolidar competencias críticas: Validar y priorizar competencias que impulsan resultados estratégicos. Integrar en gestión de talento: Implementar evaluación en talento clave, priorizar 1–2 brechas críticas por persona, definir planes de desarrollo concretos y responsabilizar a líderes por su ejecución. Gestionar cierre de brechas: Monitorear progreso, medir impacto en desempeño y comportamiento, ajustar procesos, prácticas y reglas con seguimiento formal y priorización de acciones."},
        3: {"causa": "La organización anticipa salidas y activa planes de retención, sucesión y desarrollo alineados a la estrategia", "recom": "Riesgo mínimo de pérdida de talento crítico. Alta predictibilidad en la ejecución del negocio.", "alcance": "Evaluar adopción y efectividad: Revisar uso del modelo, desempeño y resultados de la evaluación de competencias. Ajustar y alinear: Diseñar planes para cerrar brechas de adopción y reforzar competencias estratégicas según evolución del negocio. Transferir y formar líderes: Capacitar a responsable para garantizar sostenibilidad, replicabilidad y alineación estratégica. Innovación continua: Establecer mecanismos de mejora continua del modelo, integrando aprendizajes y anticipando necesidades futuras."}
    },
    15: {
        1: {"causa": "Las decisiones de talento se basan en percepción y experiencia individual, no en información objetiva.", "recom": "Brechas críticas no identificadas. Desempeño inconsistente y rotación evitable.", "alcance": "Definir competencias clave: Identificar y acordar competencias críticas alineadas con la estrategia. Diseñar evaluación: Establecer métricas, reglas y herramientas de medición. Implementar con talento clave: Evaluar competencias, identificar brechas críticas y definir planes de desarrollo iniciales para talento clave. Transferir: Capacitar responsables para garantizar sostenibilidad y uso consistente del modelo."},
        2: {"causa": "La información existe, pero no se traduce en planes de desarrollo alineados a las capacidades que exige la estrategia.", "recom": "Brechas críticas persistentes. Bajo retorno de la inversión en evaluación.", "alcance": "Consolidar competencias críticas: Validar y priorizar competencias que impulsan resultados estratégicos. Integrar en gestión de talento: Implementar evaluación en talento clave, priorizar 1–2 brechas críticas por persona, definir planes de desarrollo concretos y responsabilizar a líderes por su ejecución. Gestionar cierre de brechas: Monitorear progreso, medir impacto en desempeño y comportamiento, ajustar procesos, prácticas y reglas con seguimiento formal y priorización de acciones."},
        3: {"causa": "La organización desarrolla capacidades clave que soportan resultados actuales y futuros del negocio.", "recom": "Mayor capacidad de ejecución estratégica. Ventaja competitiva sostenible basada en talento.", "alcance": "Evaluar adopción y efectividad: Revisar uso del modelo, desempeño y resultados de la evaluación de competencias. Ajustar y alinear: Diseñar planes para cerrar brechas de adopción y reforzar competencias estratégicas según evolución del negocio. Transferir y formar líderes: Capacitar a responsable para garantizar sostenibilidad, replicabilidad y alineación estratégica. Innovación continua: Establecer mecanismos de mejora continua del modelo, integrando aprendizajes y anticipando necesidades futuras."}
    },
    16: {
        1: {"causa": "La organización carece de un marco cultural que oriente comportamientos y decisiones alineadas a la estrategia.", "recom": "Comportamientos inconsistentes. Decisiones contradictorias. Alta dependencia del estilo individual de los líderes.", "alcance": "Caracterizar la cultura y cocrear el modelo cultural: Identificar cultura actual y qué tan lejos se está de la que necesita la organización estableciendo estrategias de acción. Acompañar la implementación: Acompañar la implementación de proyecto piloto para Implementar las estrategias de transformación cultural en la empresa y garantizar la efectividad del modelo.  Monitoreo y validación: Medir impacto en comportamiento, desempeño y alineación estratégica, ajustando procesos y sistemas según resultados.   Transferencia y sostenibilidad: Capacitar a líderes y equipos para que patrocinen y repliquen la cultura en toda la organización y se mantenga la cultura."},
        2: {"causa": "Existe un marco cultural formal, pero no está incorporado en sistemas, métricas, liderazgo ni procesos clave.", "recom": "Incoherencia entre discurso y práctica. Pérdida de credibilidad interna. Desalineación entre desempeño y estrategia.", "alcance": "Caracterizar la cultura y cocrear el modelo cultural: Identificar cultura actual y qué tan lejos se está de la que necesita la organización estableciendo estrategias de acción. Acompañar la implementación: Acompañar la implementación de proyecto piloto para Implementar las estrategias de transformación cultural en la empresa y garantizar la efectividad del modelo.  Monitoreo y validación: Medir impacto en comportamiento, desempeño y alineación estratégica, ajustando procesos y sistemas según resultados."},
        3: {"causa": "La cultura guía decisiones, comportamientos y procesos; está reforzada por liderazgo, métricas, incentivos y sistemas.", "recom": "Coherencia organizacional. Decisiones alineadas. Ejecución estratégica consistente.", "alcance": "Revisión: Identificación de brechas en la adopción cultural. Plan de alineación: Diseño del plan de ajuste y alineación. Transferencia del modelo cultural: Formación avanzada de jefes y líderes patrocinadores culturales. Innovación y adaptación continua del modelo cultural: Establecer mecanismos para la adaptación continua del modelo a los cambios."}
    },
    17: {
        1: {"causa": "No existen hábitos, incentivos ni liderazgo que promuevan el uso de tecnología y datos en la toma de decisiones.", "recom": "Subutilización de inversiones tecnológicas. Decisiones intuitivas y baja competitividad. Retrasos y reprocesos en la ejecución estratégica.", "alcance": "Caracterizar la cultura: Co-creación con líderes de un modelo que impulse adopción de tecnología y datos. Acompañar la implementación: Acompañar la implementación de proyecto piloto para Implementar las estrategias de transformación cultural. Monitoreo y validación: Medir impacto en comportamiento, desempeño y alineación estratégica, ajustando procesos y sistemas según resultados. Transferencia y sostenibilidad: Transferencia de conocimiento para sostenibilidad."},
        2: {"causa": "La adopción depende de líderes o equipos específicos, sin integración sistemática en procesos y métricas.", "recom": "Ejecución desigual entre áreas. Ineficiencias y pérdida de sinergias. Decisiones inconsistentes con la estrategia.", "alcance": "Caracterizar la cultura y cocrear el modelo cultural: Identificar cultura actual y qué tan lejos se está de la que necesita la organización estableciendo estrategias de acción. Acompañar la implementación: Acompañar la implementación de proyecto piloto para Implementar las estrategias de transformación cultural en la empresa y garantizar la efectividad del modelo.  Monitoreo y validación: Medir impacto en comportamiento, desempeño y alineación estratégica, ajustando procesos y sistemas según resultados."},
        3: {"causa": "Los líderes modelan el uso de datos; los procesos, métricas y sistemas refuerzan decisiones basadas en indicadores.", "recom": "Mejor calidad de decisiones estratégicas. Mayor capacidad de adaptación y ventaja competitiva.", "alcance": "Revisión: Identificación de brechas para la adopción tecnológica y uso de datos, refuerzo de procesos y métricas, formación. Plan de alineación: Diseño del plan de ajuste y alineación. Transferencia del modelo cultural: Formación avanzada de jefes y líderes patrocinadores culturales. Innovación y adaptación continua del modelo cultural: Establecer mecanismos para la sostenibilidad. "}
    },
    18: {
        1: {"causa": "Existe una brecha entre lo que se declara y lo que se decide y ejecuta.", "recom": "Pérdida de credibilidad cultural. Equipos desalineados y bajo compromiso. Riesgo de rotación de talento clave.", "alcance": "Caracterizar la cultura y Co-creación del modelo cultural con líderes, enfatizando su rol como agentes de cambio y patrocinadores de la cultura gestión de resistencias. Acompañar la implementación: Implementación de proyecto piloto de transformación cultural con líderes. Monitoreo y validación de impacto cultural: Medir impacto en comportamiento, desempeño y alineación estratégica, ajustando procesos y sistemas.   Transferencia y sostenibilidad: transferencia de conocimiento para sostenibilidad."},
        2: {"causa": "La coherencia cultural depende de líderes individuales y no del sistema organizacional.", "recom": "Mensajes contradictorios entre equipos. Diferencias en desempeño y clima. Ejecución estratégica desigual.", "alcance": "Caracterizar la cultura y cocrear el modelo cultural: Identificar cultura actual y qué tan lejos se está de la que necesita la organización estableciendo estrategias de acción. Acompañar la implementación: Acompañar la implementación de proyecto piloto para Implementar las estrategias de liderazgo cultural.  Monitoreo y validación: Medir impacto ajustando procesos y sistemas según resultados."},
        3: {"causa": "El liderazgo actúa como principal mecanismo de transmisión cultural y alineación estratégica.", "recom": "Coherencia organizacional. Equipos alineados, comprometidos y productivos. Innovación y adaptación sostenidas.", "alcance": "Revisión: Identificación de brechas en la adopción de liderazgo cultural para el cumplimiento de la estrategia. Plan de alineación: Diseño del plan de ajuste y alineación. Transferencia del modelo cultural: Formación avanzada de jefes y líderes patrocinadores culturales. Innovación y adaptación continua del modelo cultural: Establecer mecanismos para la sostenibilidad."}
    }
}

class AppAdmin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("C-LAB SCAN PRO - Diagnóstico Sistémico Avanzado")
        self.geometry("1400x980")
        ctk.set_appearance_mode("dark")
        self.url_encuesta = "https://clab-quiz.vercel.app/"

# --- CARGA DE RECURSOS VISUALES ---
        try:
            self.logo_image = ctk.CTkImage(light_image=Image.open("logo.png"), 
                                          dark_image=Image.open("logo.png"), 
                                          size=(450, 180))
        except Exception as e:
            print(f"Error cargando imágenes: {e}")
            self.logo_image = None

        self.banco_preguntas = [
            {"t": "1. ¿Existe un plan estratégico formal, actualizado y comunicado?", "o": ["No existe plan formal.", "Plan desactualizado o comunicación parcial.", "Plan formal, actualizado y comunicado a todos."]},
            {"t": "2. ¿Los líderes asignan recursos según prioridades estratégicas?", "o": ["No asignan recursos según prioridades.", "Asignación parcial según prioridades.", "Asignación total según prioridades."]},
            {"t": "3. ¿Los planes operativos están alineados e implementados?", "o": ["No hay planes operativos alineados.", "Alineados e implementados parcialmente.", "Todos los planes alineados e implementados."]},
            {"t": "4. ¿La estructura define interacción de cargos para la estrategia?", "o": ["No define interacciones.", "Define interacciones parcialmente.", "Define todas las interacciones de cargos y roles."]},
            {"t": "5. ¿Las responsabilidades de cargos son formales y comunicadas?", "o": ["No existen responsabilidades formales.", "Algunas responsabilidades son formales.", "Todas las responsabilidades son formales y comunicadas."]},
            {"t": "6. ¿Los procesos de talento son ágiles y alineados?", "o": ["No hay procesos formales o alineados.", "Algunos procesos son ágiles y alineados.", "Todos los procesos son ágiles y alineados."]},
            {"t": "7. ¿Líderes usan datos para tomar decisiones estratégicas?", "o": ["No existen datos ni reportes formales.", "Uso parcial de indicadores y reportes.", "Uso constante de indicadores para decisiones."]},
            {"t": "8. ¿Decisiones de talento se basan en indicadores?", "o": ["No se apoya en indicadores.", "Uso parcial o esporádico.", "Uso para todas las decisiones de talento."]},
            {"t": "9. ¿Los colaboradores usan la tecnología efectivamente?", "o": ["Existen brechas significativas de adopción.", "Uso en algunos equipos sin consistencia.", "Tecnología integrada y efectiva transversalmente."]},
            {"t": "10. ¿Se mide y gestiona la experiencia del colaborador?", "o": ["No existe modelo formal.", "Modelo formal gestionado parcialmente.", "Modelo completo para medir y gestionar."]},
            {"t": "11. ¿Hay propuesta de valor (EVP) como ventaja competitiva?", "o": ["No existe EVP formal.", "Definida pero no se usa como ventaja.", "Definida y se usa como ventaja competitiva."]},
            {"t": "12. ¿Se mide el impacto del liderazgo en la experiencia?", "o": ["No se mide impacto del liderazgo.", "Se mide parcialmente el impacto.", "Se mide totalmente el impacto y retención."]},
            {"t": "13. ¿Están identificados cargos críticos y talento clave?", "o": ["No están identificados.", "Identificados algunos cargos y talentos.", "Todos los cargos y talentos clave identificados."]},
            {"t": "14. ¿Se mide y gestiona el riesgo de perder talento?", "o": ["No se mide ni gestiona.", "Se gestiona para algunos talentos.", "Se gestiona para todo el talento clave."]},
            {"t": "15. ¿Se mide competencias y gestiona el desarrollo?", "o": ["No se miden competencias.", "Se mide pero no se gestiona el desarrollo.", "Se mide y todo talento tiene plan de desarrollo."]},
            {"t": "16. ¿Cultura definida y gestionada activamente?", "o": ["Sin definición clara.", "Definida sin gestión consistente.", "Definida y gestionada activamente."]},
            {"t": "17. ¿Cultura respalda adopción tecnológica y datos?", "o": ["No respalda tecnología ni datos.", "Respaldo parcial o inconsistente.", "Impulsa consistentemente tecnología y datos."]},
            {"t": "18. ¿Líderes son referentes de valores estratégicos?", "o": ["No guían ni refuerzan comportamientos.", "Guía parcial de comportamientos.", "Guía y refuerzo consistente de valores."]}
        ]

        # Layout Sidebar
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="C-LAB SCAN", font=("Arial", 22, "bold"), text_color="#008f8c").pack(pady=40)
        ctk.CTkButton(self.sidebar, text="📝 Nuevo Diagnóstico", command=self.mostrar_cuestionario).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="📊 Dashboard Radar", command=self.mostrar_graficas).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="🔍 Buscar Persona", command=self.mostrar_buscador).pack(pady=10, padx=20)
        ctk.CTkButton(self.sidebar, text="🔗 Copiar URL", fg_color="#374151", command=self.copiar_url).pack(pady=50, padx=20)

        self.main_container = ctk.CTkScrollableFrame(self, fg_color="#1f2937") 
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.mostrar_cuestionario()

    def copiar_url(self):
        pyperclip.copy(self.url_encuesta)
        messagebox.showinfo("C-LAB SCAN", "URL copiada al portapapeles")

    def mostrar_cuestionario(self):
        for w in self.main_container.winfo_children(): w.destroy()

        if self.logo_image:
                    ctk.CTkLabel(self.main_container, image=self.logo_image, text="").pack(pady=10)        
        
        # --- SECCIÓN 1: DATOS DE CABECERA (Organizados en 3 columnas) ---
        f_header = ctk.CTkFrame(self.main_container, fg_color="#2d3748")
        f_header.pack(fill="x", padx=10, pady=10)
        f_header.grid_columnconfigure((0, 1, 2), weight=1)

        # Fila 1
        self.ent_nombre = ctk.CTkEntry(f_header, placeholder_text="Nombre del Consultor/Líder", height=35)
        self.ent_nombre.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.ent_empresa = ctk.CTkEntry(f_header, placeholder_text="Empresa Evaluada", height=35)
        self.ent_empresa.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.ent_sector = ctk.CTkEntry(f_header, placeholder_text="Sector Económico", height=35)
        self.ent_sector.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # FILA 1: País, Empleados, Antigüedad
        self.ent_pais = ctk.CTkEntry(f_header, placeholder_text="Ciudad / País", height=35)
        self.ent_pais.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.ent_empleados = ctk.CTkEntry(f_header, placeholder_text="Número de Empleados", height=35)
        self.ent_empleados.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.ent_antiguedad = ctk.CTkEntry(f_header, placeholder_text="Antigüedad de la Empresa", height=35)
        self.ent_antiguedad.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # --- SECCIÓN 2: CONTEXTO Y RETOS ---
        f_contexto = ctk.CTkFrame(self.main_container, fg_color="transparent")
        f_contexto.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(f_contexto, text="1. ¿Cuál es el reto estratégico y de talento qué tiene su organización?", 
                     font=("Arial", 12, "bold"), text_color="#008f8c").pack(anchor="w", padx=10)
        self.txt_reto1 = ctk.CTkTextbox(f_contexto, height=70, border_width=1, border_color="#4a5568")
        self.txt_reto1.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(f_contexto, text="2. ¿Qué acciones se han tomado hoy para hacerle frente a este reto y cual ha sido su efectividad?", 
                     font=("Arial", 12, "bold"), text_color="#008f8c").pack(anchor="w", padx=10)
        self.txt_reto2 = ctk.CTkTextbox(f_contexto, height=70, border_width=1, border_color="#4a5568")
        self.txt_reto2.pack(fill="x", padx=10, pady=(0, 10))

        # --- SECCIÓN 3: CUESTIONARIO (18 Preguntas completas) ---
        self.resp_vars = []
        for p in self.banco_preguntas:
            f = ctk.CTkFrame(self.main_container, fg_color="#374151")
            f.pack(fill="x", pady=5, padx=10)
            
            # Texto de la pregunta
            ctk.CTkLabel(f, text=p["t"], font=("Arial", 14, "bold"), text_color="#008f8c", 
                         wraplength=1000, justify="left").pack(anchor="w", padx=20, pady=5)
            
            v = ctk.StringVar(value="0")
            self.resp_vars.append(v)
            
            # Opciones literales del banco de preguntas
            for idx, opt in enumerate(p["o"]):
                ctk.CTkRadioButton(f, text=opt, variable=v, value=str(idx+1)).pack(anchor="w", padx=45, pady=2)
        
        # Botón de cierre
        ctk.CTkButton(self.main_container, text="FINALIZAR Y ANALIZAR", 
                      command=self.enviar_datos, height=50, font=("Arial", 16, "bold")).pack(pady=40)

    def enviar_datos(self):
        resps = {f"p{i+1}": int(v.get()) for i, v in enumerate(self.resp_vars)}
        if 0 in resps.values() or not self.ent_nombre.get(): return messagebox.showwarning("Atención", "Por favor completa todas las respuestas y datos.")
        data = {"nombre": self.ent_nombre.get(), "empresa": self.ent_empresa.get(), "respuestas": resps, "fecha": datetime.now().isoformat()}
        db.child("calificaciones").push(data)
        self.generar_dashboard(data)

    def generar_dashboard(self, data):
        for w in self.main_container.winfo_children(): w.destroy()

        # --- DIBUJAR LOGO ---
        if self.logo_image:
            ctk.CTkLabel(self.main_container, image=self.logo_image, text="", fg_color="transparent").pack(pady=30)

        ctk.CTkLabel(self.main_container, text=f"DASHBOARD SISTÉMICO: {data['empresa'].upper()}", font=("Arial", 24, "bold"), text_color="#008f8c").pack(pady=20)
        
        resp = data['respuestas']
        dimensiones = {
            "Estrategia": [1, 2, 3], "Procesos y Org.": [4, 5, 6], "Datos y Tecnología": [7, 8, 9],
            "Experiencia Colab.": [10, 11, 12], "Personas": [13, 14, 15], "Cultura": [16, 17, 18]
        }
        dims_nombres = list(dimensiones.keys())
        vals = [sum(resp[f"p{i}"] for i in dimensiones[d])/3 for d in dims_nombres]
        brechas = [3.0 - v for v in vals]

        # --- TABLA DE BRECHAS ---
# --- TABLA DE BRECHAS ---
        t_frame = ctk.CTkFrame(self.main_container, fg_color="#2d3748")
        t_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(t_frame, text="RESUMEN ESTRATÉGICO DE BRECHAS", font=("Arial", 16, "bold"), text_color="#43a3a8").pack(pady=10)
        
        # 1. ACTUALIZACIÓN DE ENCABEZADOS (Añadimos "NIVEL DE URGENCIA")
        h_frame = ctk.CTkFrame(t_frame, fg_color="transparent")
        h_frame.pack(fill="x", padx=20)
        headers = ["DIMENSIÓN", "PUNTAJE PROMEDIO", "BRECHA (GAP)", "NIVEL DE URGENCIA"]
        for i, head in enumerate(headers):
            # Ajustamos el ancho (width) a 200 para que quepan 4 columnas cómodamente
            ctk.CTkLabel(h_frame, text=head, font=("Arial", 11, "bold"), text_color="#94a3b8", width=200).grid(row=0, column=i, padx=5, pady=5)

        # Filas de la tabla por dimensión
        for i, nombre_dim in enumerate(dims_nombres):
            fila = ctk.CTkFrame(t_frame, fg_color="#1e293b" if i % 2 == 0 else "#2d3748")
            fila.pack(fill="x", padx=10, pady=2)
            
            puntaje_prom = vals[i]
            brecha_valor = 3.0 - puntaje_prom

            # 2. LÓGICA DE NIVEL DE URGENCIA Y COLORES
            if 0.1 <= brecha_valor <= 1.0:
                urgencia_texto = "BAJO"
                color_urgencia = "#34d399" # Verde
            elif 1.1 <= brecha_valor <= 1.9:
                urgencia_texto = "MEDIO"
                color_urgencia = "#fbbf24" # Amarillo/Naranja
            elif brecha_valor >= 2.0:
                urgencia_texto = "ALTO"
                color_urgencia = "#f87171" # Rojo
            else:
                urgencia_texto = "N/A" # Para brechas de 0.0
                color_urgencia = "#94a3b8"
            
            # Columna Dimensión
            ctk.CTkLabel(fila, text=nombre_dim.upper(), font=("Arial", 11, "bold"), width=200, anchor="w").grid(row=0, column=0, padx=20, pady=5)
            
            # Columna Puntaje
            ctk.CTkLabel(fila, text=f"{puntaje_prom:.2f} / 3.0", width=200).grid(row=0, column=1, padx=5)
            
            # Columna Brecha
            ctk.CTkLabel(fila, text=f"{brecha_valor:.2f}", width=200).grid(row=0, column=2, padx=5)
            
            # 3. NUEVA COLUMNA: NIVEL DE URGENCIA (Con color condicional)
            ctk.CTkLabel(fila, text=urgencia_texto, font=("Arial", 12, "bold"), text_color=color_urgencia, width=200).grid(row=0, column=3, padx=5)

        # Radar Plot (Se mantiene igual debajo de la tabla)
        fig, ax = plt.subplots(figsize=(5, 4), subplot_kw=dict(polar=True))
        
# --- MEJORA DEL GRÁFICO DE RADAR CON DECIMALES Y PORCENTAJE ---
        fig, ax = plt.subplots(figsize=(8, 7), subplot_kw=dict(polar=True))
        fig.patch.set_facecolor('#1f2937')
        ax.set_facecolor('#111827')
        fig.subplots_adjust(left=0.15, right=0.85, top=0.85, bottom=0.15)
        # Datos y Cierre del Polígono
        angles = np.linspace(0, 2*np.pi, len(dims_nombres), endpoint=False).tolist()
        stats = vals + [vals[0]]
        angles_closed = angles + [angles[0]]
        
        # Cálculo del Promedio Porcentual General (Base 3.0)
        promedio_general = sum(vals) / len(vals)
        cumplimiento_porcentaje = (promedio_general / 3.0) * 100

        # Dibujar área y bordes
        ax.fill(angles_closed, stats, color='#3b82f6', alpha=0.4, edgecolor='#60a5fa', linewidth=2)
        ax.plot(angles_closed, stats, color='#60a5fa', linewidth=2, marker='o', markersize=4)
        
        # Meta Ideal (3.0)
        ax.plot(angles_closed, [3.0]*len(angles_closed), color='#f87171', linestyle='--', alpha=0.8, label="Meta Ideal (3.0)")

        # --- MOSTRAR VALORES DECIMALES EN LOS PUNTOS ---
        for angle, val in zip(angles, vals):
            # Posicionamos el texto ligeramente arriba del punto (val + 0.15)
            ax.text(angle, val + 0.25, f'{val:.2f}', color="#f6f6f6", 
                    fontweight='bold', fontsize=10, ha='center', va='center')

        # --- AÑADIR PROMEDIO PORCENTUAL EN EL CENTRO ---
        # Usamos un texto flotante en el centro del gráfico (o en el título)
        plt.title(f"CUMPLIMIENTO TOTAL: {cumplimiento_porcentaje:.1f}%", 
                  color='#008f8c', fontsize=16, fontweight='bold', pad=30)

        # Configuración de escala
        ax.set_ylim(0, 3.5) # Margen para los números decimales
        ax.set_yticks([1, 2, 3])
        ax.set_yticklabels(["1", "2", "3"], color="#94a3b8", size=8)
        ax.grid(True, color="#374151", linestyle='--')

        # Etiquetas de dimensiones (Nombres)
        ax.set_xticks(angles)
        ax.set_xticklabels(dims_nombres, color="white", size=9, weight='bold')
        
        # Ajuste de posición de etiquetas para evitar solapamiento
        for label, angle in zip(ax.get_xticklabels(), angles):
            if 0 <= angle < np.pi:
                label.set_horizontalalignment('left')
            else:
                label.set_horizontalalignment('right')

        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=1, 
                  fontsize=9, facecolor='#1f2937', edgecolor='#4b5563', labelcolor='white')

        # Renderizado
        canvas = FigureCanvasTkAgg(fig, master=self.main_container)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20, padx=10)

        # --- RECOMENDACIONES DETALLADAS CON RESPUESTA AL FRENTE ---
        for i in range(1, 19):
            p_val = resp[f"p{i}"]
            info = MATRIZ_EXCEL[i][p_val]
            pregunta_texto = self.banco_preguntas[i-1]['t']
            respuesta_seleccionada = self.banco_preguntas[i-1]['o'][p_val-1]
            
            card = ctk.CTkFrame(self.main_container, fg_color="#2d3748", border_width=1, border_color="#4a5568")
            card.pack(fill="x", padx=20, pady=10)
            
            # Header del Punto de Control
            h = ctk.CTkFrame(card, fg_color="#1e293b")
            h.pack(fill="x", padx=2, pady=2)
            ctk.CTkLabel(h, text=f"PUNTO DE CONTROL {i}", font=("Arial", 12, "bold"), text_color="#008f8c").pack(side="left", padx=15)
            ctk.CTkLabel(h, text=f"Puntaje: {p_val}/3", font=("Arial", 11, "bold")).pack(side="right", padx=15)

            # Texto de la Pregunta
            ctk.CTkLabel(card, text=pregunta_texto, font=("Arial", 14, "bold"), text_color="white", wraplength=1100, justify="left").pack(anchor="w", padx=20, pady=(10, 5))
            
            # SECCIÓN: LO QUE SE RESPONDIÓ
            resp_box = ctk.CTkFrame(card, fg_color="#334155", corner_radius=5)
            resp_box.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(resp_box, text=f"🔘 Respuesta capturada: {respuesta_seleccionada}", font=("Arial", 13, "italic"), text_color="#93c5fd").pack(anchor="w", padx=15, pady=5)

            # Contenido del Excel
            ctk.CTkLabel(card, text="🚩 INTERPRETACIÓN:", font=("Arial", 11, "bold"), text_color="#fbbf24").pack(anchor="w", padx=25, pady=(10, 0))
            ctk.CTkLabel(card, text=info['causa'], wraplength=1100, justify="left", font=("Arial", 12)).pack(anchor="w", padx=45, pady=(0, 10))
            
            ctk.CTkLabel(card, text="💡 POSIBLES CONSECUENCIAS:", font=("Arial", 11, "bold"), text_color="#34d399").pack(anchor="w", padx=25)
            ctk.CTkLabel(card, text=info['recom'], wraplength=1100, justify="left", font=("Arial", 12)).pack(anchor="w", padx=45, pady=(0, 10))
            
            ctk.CTkLabel(card, text="🎯 RECOMENDACIÓN:", font=("Arial", 11, "bold"), text_color="#60a5fa").pack(anchor="w", padx=25)
            ctk.CTkLabel(card, text=info['alcance'], wraplength=1100, justify="left", font=("Arial", 12)).pack(anchor="w", padx=45, pady=(0, 15))

    def mostrar_buscador(self):
        for w in self.main_container.winfo_children(): w.destroy()
        ctk.CTkLabel(self.main_container, text="HISTORIAL DE EVALUACIONES", font=("Arial", 22, "bold")).pack(pady=25)
        try:
            data = db.child("calificaciones").get().val()
            if data:
                for k, v in data.items(): # type: ignore
                    emp = v.get('empresa', 'N/A')
                    nom = v.get('nombre', 'N/A')
                    fec = v.get('fecha', '')[:10]
                    ctk.CTkButton(self.main_container, text=f"📅 {fec} | 🏢 {emp} | 👤 Eval: {nom}", 
                                   command=lambda d=v: self.generar_dashboard(d), height=35).pack(fill="x", pady=4, padx=50)
            else:
                ctk.CTkLabel(self.main_container, text="No hay registros.").pack()
        except:
            ctk.CTkLabel(self.main_container, text="Error de conexión.").pack()

    def mostrar_graficas(self):
        try:
            data = db.child("calificaciones").get().val()
            if data: self.generar_dashboard(list(data.values())[-1]) # type: ignore
        except: pass

if __name__ == "__main__":
    app = AppAdmin()
    app.mainloop()