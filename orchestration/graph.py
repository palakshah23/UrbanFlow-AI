from langgraph.graph import StateGraph, START, END

from orchestration.state import UrbanFlowState

from agents.perception import perception_agent
from agents.prediction import prediction_agent
from agents.emergency_routing import emergency_routing_agent
from agents.signal_coordination import signal_coordination_agent
from agents.citizen_advisory import citizen_advisory_agent

from trust.validation import validation_agent


def build_urbanflow_graph():
    """
    Build and compile the UrbanFlow AI multi-agent workflow.
    """

    graph = StateGraph(UrbanFlowState)

    # Add agents
    graph.add_node("perception", perception_agent)
    graph.add_node("prediction", prediction_agent)
    graph.add_node(
        "emergency_routing",
        emergency_routing_agent
    )
    graph.add_node(
        "signal_coordination",
        signal_coordination_agent
    )
    graph.add_node(
        "validation",
        validation_agent
    )
    graph.add_node(
        "citizen_advisory",
        citizen_advisory_agent
    )

    # Define workflow
    graph.add_edge(
        START,
        "perception"
    )

    graph.add_edge(
        "perception",
        "prediction"
    )

    graph.add_edge(
        "prediction",
        "emergency_routing"
    )

    graph.add_edge(
        "emergency_routing",
        "signal_coordination"
    )

    graph.add_edge(
        "signal_coordination",
        "validation"
    )

    graph.add_edge(
        "validation",
        "citizen_advisory"
    )

    graph.add_edge(
        "citizen_advisory",
        END
    )

    return graph.compile()