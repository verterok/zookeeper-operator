#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

from unittest.mock import patch

from utils import get_env, update_env

from src.utils import map_env


def test_map_env_populated():
    example_env = [
        "KAFKA_OPTS=orcs -Djava=wargs -Dkafka=goblins",
        "SERVER_JVMFLAGS=dwarves -Djava=elves -Dzookeeper=men",
    ]
    env = map_env(env=example_env)

    assert len(env) == 2
    assert sorted(env.keys()) == sorted(["KAFKA_OPTS", "SERVER_JVMFLAGS"])

    for value in env.values():
        assert type(value) == str
        # checks handles multiple equals signs in value
        assert len(value.split()) == 3


def test_get_env_empty():
    with patch("utils.safe_get_file", return_value=[]):
        assert not get_env()
        assert get_env() == {}


def test_update_env():
    example_get_env = {
        "KAFKA_OPTS": "orcs -Djava=wargs -Dkafka=goblins",
        "SERVER_JVMFLAGS": "dwarves -Djava=elves -Dzookeeper=men",
    }
    example_update_env = {
        "SERVER_JVMFLAGS": "gimli -Djava=legolas -Dzookeeper=aragorn",
    }

    with (
        patch("utils.get_env", return_value=example_get_env),
        patch("utils.safe_write_to_file") as safe_write,
    ):
        update_env(env=example_update_env)

        assert all(
            updated in safe_write.call_args.kwargs["content"]
            for updated in ["gimli", "legolas", "aragorn"]
        )
        assert "KAFKA_OPTS" in safe_write.call_args.kwargs["content"]
        assert safe_write.call_args.kwargs["path"] == "/etc/environment"
        assert safe_write.call_args.kwargs["mode"] == "w"
