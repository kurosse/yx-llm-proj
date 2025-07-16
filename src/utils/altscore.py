def get_altscores(data, g_weight=0.25, s_weight=0.15, c_weight=0.60):
    """
    Generates the altscore for each candidate in the dataset.
    """
    score_mapping = {
        "Excellent": 10,
        "Near-Excellent": 9,
        "Very Good": 8,
        "Good": 7,
        "Slightly Above Acceptable": 6,
        "Acceptable": 5,
        "Fair": 4,
        "Poor": 3,
        "Very Poor": 2,
        "Unacceptable": 1,
    }

    altscores = {
        f"candidate_{i+1}": {}
        for i in range(len(data["candidate_sentence_evaluations"]))
    }

    for index, candidate in enumerate(data["candidate_sentence_evaluations"]):
        # Fluency agent rating
        grammar_score = score_mapping[
            candidate["fluency_agent_response"]["grammar_rating"]
        ]
        spelling_score = score_mapping[
            candidate["fluency_agent_response"]["spelling_rating"]
        ]

        # Cultural agent rating
        if candidate["cultural_agent_response"]["cultural_items_and_clues"] is None:
            # Renormalize the weights for grammar and spelling if cultural items are not provided
            total_weight = g_weight + s_weight
            g_weight = g_weight / total_weight
            s_weight = s_weight / total_weight
            cultural_score = 0.0  # No cultural score if no items are provided
        else:
            cultural_core_score = score_mapping[
                candidate["cultural_agent_response"]["cultural_accuracy_rating"]
            ]
            coverage_factor = len(
                [
                    cultural_translation["translated_correctly"] is True
                    for cultural_translation in candidate["cultural_agent_response"][
                        "cultural_items_and_clues"
                    ]
                ]
            ) / len(candidate["cultural_agent_response"]["cultural_items_and_clues"])
            cultural_score = cultural_core_score * coverage_factor

        # Generate the altscore
        altscore = (
            g_weight * grammar_score
            + s_weight * spelling_score
            + c_weight * cultural_score
        ) * 10  # Scale to 0-100

        altscores[f"candidate_{index+1}"] = {
            "translation": candidate["candidate_sentence"],
            "altscore": altscore,
            "grammar_score": grammar_score,
            "spelling_score": spelling_score,
            "cultural_score": cultural_score,
            "weights": {
                "grammar_weight": g_weight,
                "spelling_weight": s_weight,
                "cultural_weight": c_weight,
            },
        }

    return altscores
