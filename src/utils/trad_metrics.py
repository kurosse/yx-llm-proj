import multiprocessing as mp
import logging

import evaluate
import sacrebleu


class TradMetrics:
    """
    A class to handle translation metrics evaluation.
    It supports BLEU, CHRF, and COMET metrics.
    """

    def __init__(self):
        self.bleu = evaluate.load("bleu")
        self.chrf = evaluate.load("chrf")
        self.comet = evaluate.load("comet")

        try:
            mp.set_start_method("spawn", force=True)
        except RuntimeError:
            pass

        logging.getLogger("lightning.pytorch.utilities.rank_zero").setLevel(
            logging.ERROR
        )
        # For older Lightning versions, you may also need:
        logging.getLogger("pytorch_lightning.utilities.rank_zero").setLevel(
            logging.ERROR
        )

    def calculate_single_ref_score(self, model, predictions, reference, source=None):
        """
        COMET requires the source text in the original language.
        """

        scores = []
        for prediction in predictions:

            match model:
                # case "bleu":
                #     scores.append(bleu.compute(predictions=[prediction], references=[reference]))
                case "sentence_bleu":
                    scores.append(
                        sacrebleu.sentence_bleu(prediction, [reference]).score
                    )
                case "chrf":
                    scores.append(
                        self.chrf.compute(
                            predictions=[prediction], references=[reference]
                        )["score"]
                    )
                case "comet":
                    if source is None:
                        raise ValueError("COMET requires source texts for scoring.")
                    scores.append(
                        self.comet.compute(
                            predictions=[prediction],
                            references=[reference],
                            sources=[source],
                            gpus=1,
                            progress_bar=False,
                        )["scores"][0]
                    )
                case _:
                    raise ValueError(f"Unknown model: {model}")

        return scores

    def review_all_models(self, predictions, reference, sources=None):
        """
        Calculate scores for all predictions against their corresponding references.
        If sources are provided, they will be used for COMET scoring.
        """
        scores = {"sentence_bleu": [], "chrf": [], "comet": []}

        for k, v in scores.items():
            result = self.calculate_single_ref_score(k, predictions, reference, sources)
            scores[k] = result

        return scores
