# Lint as: python2, python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A Metadata adapter class used to add Kubeflow-specific context."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from typing import Any, Dict, Text
import absl

from ml_metadata.proto import metadata_store_pb2
from tfx.orchestration import data_types
from tfx.orchestration import metadata

_KFP_POD_NAME_KEY = 'KFP_POD_NAME'

_ARTIFACT_TYPE_VERSION = 2
_EXECUTION_TYPE_VERSION = 1


class KubeflowMetadataAdapter(metadata.Metadata):
  """A Metadata adapter class for orchestrations run using KFP.

  This is used to add properties to artifacts and executions, such as the Argo
  workflow ID and kubernetes pod IDs.
  """

  def _prepare_execution(
      self,
      state: Text,
      exec_properties: Dict[Text, Any],
      pipeline_info: data_types.PipelineInfo,
      component_info: data_types.ComponentInfo,
  ) -> metadata_store_pb2.Execution:
    component_info.component_type = component_info.component_type + '-Kubeflow-V' + str(
        _EXECUTION_TYPE_VERSION)
    exec_properties['pod_name'] = metadata_store_pb2.STRING
    execution = super(KubeflowMetadataAdapter,
                      self)._prepare_execution(state, exec_properties,
                                               pipeline_info, component_info)
    if os.environ[_KFP_POD_NAME_KEY]:
      kfp_pod_name = os.environ[_KFP_POD_NAME_KEY]
      absl.logging.info('Adding KFP pod name %s to execution' % kfp_pod_name)
      execution.properties['pod_name'].string_value = kfp_pod_name
    return execution
